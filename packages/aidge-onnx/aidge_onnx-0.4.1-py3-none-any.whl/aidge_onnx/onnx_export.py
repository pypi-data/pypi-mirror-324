"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""
import aidge_core
import numpy as np
import sys
from typing import List, Mapping
from collections import defaultdict


from importlib.metadata import version
import onnx
from onnx import helper
from onnx import numpy_helper
from onnx import TensorProto
from aidge_onnx.utils import _AIDGE_DOMAIN

from .node_export.aidge_converter import AIDGE_NODE_CONVERTER_
from aidge_onnx import dtype_converter

def remove_duplicate_names(graph_view: aidge_core.GraphView):
    """Given a :py:class:`aidge_core.GraphView` rename every nodes with duplicate names.
    Nodes are browsed in no particular order so renaming may seems random.
    If same names are encountered the old name is suffixed by ``_{idx}``.
    Where idx in range(nb_duplicate).
    This function is called recursively as long as there are duplicates.

    :param graph_view: GraphView to parse
    :type graph_view: :py:class:`aidge_core.GraphView`
    """
    # Boolean used to get out of recursion
    name_updated = False
    # Dictionnary which map a name to the nodes which have this name
    # Use of defaultdict to ease the synthax
    name_map = defaultdict(list)
    for aidge_node in graph_view.get_nodes():
        name_map[aidge_node.name()].append(aidge_node)

    for name, node_list in name_map.items():
        if len(node_list) > 1:
            # We need another recursive call to check current modifications doesn't invalidate the graph
            name_updated = True
            for idx, node in enumerate(node_list):
                node.set_name(name + f"_{idx}")

    # Recursion call !
    if name_updated:
        remove_duplicate_names(graph_view)


def export_onnx(graph_view: aidge_core.GraphView,
                path_to_save: str,
                inputs_dims: Mapping[str, List[List[int]]] = None,
                outputs_dims: Mapping[str, List[List[int]]] = None,
                verbose: bool = False,
                enable_custom_op: bool = False,
                opset: int = None):
    """Export a :py:class:`aidge_core.GraphView` to an ONNX file.

    :param graph_view: :py:class:`aidge_core.GraphView` to convert.
    :type graph_view: :py:class:`aidge_core.GraphView`
    :param path_to_save: Path where to save the ONNX file, example ``test.onnx``
    :type path_to_save: str
    :param inputs_dims: input dimensions of the network, if provided, ``outputs_dims`` must also be filled, this argument is a map, where the key is the name of the input node and the value is a list of dimensions ordered by the input index, defaults to None
    :type inputs_dims: Mapping[str, List[List[int]]], optional
    :param outputs_dims: output dimensions of the network, if provided, ``inputs_dims`` must also be filled, this argument is a map, where the key is the name of the output node and the value is a list of dimensions ordered by the output index, defaults to None
    :type outputs_dims: Mapping[str, List[List[int]]], optional
    :param verbose: If true, verbosity is activated, defaults to False
    :type verbose: bool, optional
    :param enable_custom_op: If True, export will not fail for :py:class:`aidge_core.GenericOperator` and will add the operator schema to a custom aidge domain, defaults to False
    :type enable_custom_op: bool, optional
    :param opset: The version of the ONNX opset generated, defaults to None
    :type opset: int, optional
    """
    major, minor = onnx.__version__.split(".")[:2]
    if enable_custom_op and (int(major)*100 + int(minor) < 114):
        ("Warning: Cannot enable custom operator with onnx < 1.14, update onnx library with:"
              "\n\t> pip install --upgrade onnx\nDefaulting to enable_custom_op = False")
        enable_custom_op = False
    if opset is None:
        opset = onnx.defs.onnx_opset_version()

    # Map old inputs names to nodes to keep track of node name after potential renaming
    # This is used to make inputs_dims and outputs_dims works.
    old_io_names = {}
    old_io_names.update({node: node.name()
                        for node in graph_view.get_input_nodes()})
    old_io_names.update({node: node.name()
                        for node in graph_view.get_output_nodes()})

    remove_duplicate_names(graph_view)

    # Initializing variables necessary for ONNX creation
    onnx_inputs = []  # List of ONNX tensor representing graph inputs
    onnx_outputs = []  # List of ONNX tensor representing graph outputs
    onnx_initializers = []  # List of ONNX initializers in no particular order
    onnx_nodes = []  # List of ONNX nodes, must follow the topological order of the graph
    # Variable used to help in the creation of the ONNX
    open_nodes = []  # Queue of Aidge nodes to explore, guarantee a topological exploration of the graph
    closed_nodes = []  # List of Aidge nodes already explored

    if inputs_dims is None != outputs_dims is None:
        raise RuntimeError("Both input_dims and output_dims must be defined.")
    forwad_dims_required = inputs_dims is None
    if forwad_dims_required:
        for input_node in graph_view.get_input_nodes():
            for parent_node, _ in input_node.inputs():
                if parent_node is None:
                    raise RuntimeError(
                        f"One of the input of the GraphView is not set. Check {input_node.name()} inputs.")
        graph_view.forward_dims()

    open_nodes = list(graph_view.get_input_nodes())
    if not open_nodes:
        open_nodes = [graph_view.root_node()]

    graph_inputs_name = [node.name() for node in graph_view.get_input_nodes()]
    graph_outputs_name = [node.name()
                          for node in graph_view.get_output_nodes()]

    # Creating initializer list
    for aidge_node in graph_view.get_nodes():
        aidge_operator = aidge_node.get_operator()
        # Check if operator is an initializer
        if isinstance(aidge_operator, aidge_core.ProducerOp):
            if aidge_operator.get_output(0).has_impl():
                if not aidge_operator.attr.constant:
                    aidge_core.Log.info(f"Creating initializer: {aidge_node.name()}")
                    onnx_initializers.append(
                        numpy_helper.from_array(
                            np.array(aidge_operator.get_output(0)),
                            f"{aidge_node.name()}_out0")
                    )
                    # Node converted, adding to close list
                    closed_nodes.append(aidge_node)
            else:
                raise RuntimeError(f"The producer {aidge_node.name()} does not have an implementation, make sure it is initialized !")
    # Topological exploration of the graph !
    while open_nodes:
        aidge_node = open_nodes.pop(0)
        if aidge_node in closed_nodes:
            continue  # Node already converted, moving on ...
        parents_not_converted = False
        # Check all parents have been converted
        for parent in aidge_node.get_parents():
            if parent is not None and \
                    parent not in closed_nodes:
                # If parents have not been converted, push back current node
                if not parents_not_converted:
                    open_nodes.insert(0, aidge_node)
                    parents_not_converted = True
                # Add to the stack the not converted parent as next node to convert
                open_nodes.insert(0, parent)
        if parents_not_converted:
            continue
        # Next nodes to treat are children of current node
        open_nodes += list(aidge_node.get_children())
        if verbose:
            print(aidge_node.name() + "[" + aidge_node.type() + "]" + "\n" +
                  "="*(len(aidge_node.name()) + 2 + len(aidge_node.type())))

        aidge_operator = aidge_node.get_operator()

        # Set input and output names
        # /!\ IMPORTANT /!\
        # Convention:
        # - names of output is "{current_node_name}_out_{out_idx}"
        # - names of input refer to the output name set by the parent node
        node_inputs_name = []
        node_outputs_name = []

        for input_idx, input_tuple in enumerate(aidge_node.inputs()):
            # Note: input_tuple = (parent_node, parent_output_idx)
            if aidge_node.name() in graph_inputs_name and (aidge_node.input_category(input_idx) in [aidge_core.InputCategory.Data, aidge_core.InputCategory.OptionalData]):
                if aidge_node.input(input_idx)[0] in graph_view.get_nodes():
                    node_inputs_name.append(
                        f"{input_tuple[0].name()}_out{input_tuple[1]}")
                else:
                    node_inputs_name.append(
                        f"{aidge_node.name()}_in{input_idx}")
            elif input_tuple[0] is not None:
                node_inputs_name.append(
                    f"{input_tuple[0].name()}_out{input_tuple[1]}")
            elif (
                verbose
            ):  # TODO: Should this raise error or is it ok to have dangling inputs ?
                print(
                    f"Warning: {aidge_node.name()}[{input_idx}] is an unconnected input and the node is not an input of the graph."
                )
            #else:  # TODO: Should this raise error or is it ok to have dangling inputs ?
            #    raise RuntimeError(
            #        f"{aidge_node.name()}[{input_idx}] is an unconnected input and the node is not an input of the graph.")
        out_idx = 0
        for output in aidge_node.outputs():
            out_name = f"{aidge_node.name()}_out{out_idx}"
            for output_tuple in output:
                if output_tuple[0] is not None and out_name not in node_outputs_name:
                    node_outputs_name.append(out_name)
                # else:
                #     raise RuntimeError(f"{aidge_node.name()} is not an output of the graph and has no children.")
            out_idx += 1

        # Check if node is at the Output of the graph
        if aidge_node.name() in graph_outputs_name:
            # If it is the case, we create ONNX tensor for each one of the node outputs
            for i in range(aidge_node.get_nb_outputs()):
                # Check if node output are connected or not connected to an output of the graph
                if aidge_node.output(i) == [] or all([(tuple_node_idx[0] not in graph_view.get_nodes()) for tuple_node_idx in aidge_node.output(i)]):
                    output_name = f"{aidge_node.name()}_out{i}"
                    output_dims = None
                    out_dtype = None
                    if forwad_dims_required:
                        output_tensor = aidge_operator.get_output(i)
                        output_dims = output_tensor.dims()
                        out_dtype = dtype_converter.aidge_to_onnx(output_tensor.dtype())
                    else:
                        if outputs_dims is None or old_io_names[aidge_node] not in outputs_dims:
                            raise RuntimeError(
                                f"Graph output: {old_io_names[aidge_node]} has no dims specified in outputs_dims parameter.")
                        output_dims = outputs_dims[old_io_names[aidge_node]][i]
                        out_dtype = TensorProto.FLOAT  # TODO: Find a better way to get datatype
                    onnx_outputs.append(
                        helper.make_tensor_value_info(
                            output_name,
                            out_dtype,
                            output_dims
                        )
                    )
                    # Graph output is a leaf so we did not add a node_outputs_name
                    node_outputs_name.append(output_name)
        # Check if node is at the Input
        if aidge_node.name() in graph_inputs_name:
            # If it is the case, we create ONNX tensor for each one of the node inputs
            for i in range(aidge_node.get_nb_inputs()):
                if aidge_node.input_category(i) not in [aidge_core.InputCategory.Data, aidge_core.InputCategory.OptionalData]:
                    continue
                if aidge_node.input(i)[0] in graph_view.get_nodes():
                    continue  # This node input is not an input graph
                input_name = f"{aidge_node.name()}_in{i}"
                input_dims = None
                in_dtype = None
                if forwad_dims_required:
                    input_tensor = aidge_operator.input(i)
                    input_dims = input_tensor.dims()
                    in_dtype = dtype_converter.aidge_to_onnx(input_tensor.dtype())
                else:
                    if old_io_names[aidge_node] not in inputs_dims:
                        raise RuntimeError(
                            f"Graph input: {old_io_names[aidge_node]} has no dims specified in inputs_dims parameter.")
                    if i >= len(inputs_dims[old_io_names[aidge_node]]):
                        raise RuntimeError(
                            f"Graph input: {old_io_names[aidge_node]} has been described with {len(inputs_dims[old_io_names[aidge_node]])} inputs but it has {aidge_node.get_data_inputs().size()} inputs.")

                    input_dims = inputs_dims[old_io_names[aidge_node]][i]
                    in_dtype = TensorProto.FLOAT  # TODO: Find a better way to get datatype
                onnx_inputs.append(
                    helper.make_tensor_value_info(
                        input_name,
                        in_dtype,
                        input_dims
                    )
                )

        if verbose:
            print(f"\tInputs: {node_inputs_name}")
            print(f"\tOutputs: {node_outputs_name}")

        new_nodes = AIDGE_NODE_CONVERTER_[aidge_node.type()](
            aidge_node,
            node_inputs_name,
            node_outputs_name,
            opset=opset,
            verbose=verbose,
            enable_custom_op=enable_custom_op
        )
        # Add to list of onnx nodes
        onnx_nodes += new_nodes
        # Node converted, adding to close list
        closed_nodes.append(aidge_node)

    # Create the graph (GraphProto)
    onnx_graph = onnx.helper.make_graph(
        nodes=onnx_nodes,
        initializer=onnx_initializers,
        name=path_to_save,
        inputs=onnx_inputs,
        outputs=onnx_outputs,
    )
    opset_import = []
    if enable_custom_op:
        opset_import.append(helper.make_opsetid(_AIDGE_DOMAIN, 1))
    if opset:
        opset_import.append(onnx.helper.make_opsetid("", opset))

    # Create the model (ModelProto)
    onnx_model = onnx.helper.make_model(
        onnx_graph,
        producer_name=vars(sys.modules[__name__])['__package__'],
        producer_version=str(version("aidge_onnx")),
        opset_imports=opset_import
    )
    onnx.save(onnx_model, path_to_save)
