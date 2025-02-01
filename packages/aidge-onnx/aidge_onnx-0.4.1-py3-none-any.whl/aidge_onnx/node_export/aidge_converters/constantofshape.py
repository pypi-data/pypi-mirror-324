"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

from typing import List

import onnx
from onnx import helper

import aidge_core
from aidge_onnx.node_export import auto_register_export
from aidge_onnx import dtype_converter

@auto_register_export("ConstantOfShape")
def export_maxpooling(
    aidge_node: aidge_core.Node,
    node_inputs_name,
    node_outputs_name,
    opset: int = None,
    verbose: bool = False,
    **kwargs,
) -> List[aidge_core.Node]:
    aidge_operator = aidge_node.get_operator()
    aidge_value_attr: aidge_core.Tensor = aidge_operator.attr.get_attr("value")
    onnx_node = helper.make_node(
        name=aidge_node.name(),
        op_type="ConstantOfShape",
        inputs=node_inputs_name,
        outputs=node_outputs_name,
    )

    onnx_value_attr: onnx.TensorProto = helper.make_tensor_value_info(
        "value",
        dtype_converter.aidge_to_onnx(aidge_value_attr.dtype),
        [aidge_value_attr.get(0)]
    )

    onnx_node.attribute.append(helper.make_attribute("value", onnx_value_attr))
    return [onnx_node]

