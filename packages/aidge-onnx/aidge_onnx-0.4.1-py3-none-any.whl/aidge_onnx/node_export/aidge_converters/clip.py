"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import aidge_core
from onnx import helper
from aidge_onnx.node_export import auto_register_export

@auto_register_export("Clip")
def export_clip(
    aidge_node: aidge_core.Node,
    node_inputs_name,
    node_outputs_name,
    opset:int = None,
    verbose: bool = False,
    **kwargs) -> None:
    onnx_node = helper.make_node(
        name=aidge_node.name(),
        op_type="Clip",
        inputs=node_inputs_name,
        outputs=node_outputs_name,
    )
    if opset is not None and opset < 11 :
        onnx_node.attribute.append(
            helper.make_attribute(
                "min",
                aidge_node.get_operator().min()
        ))
        onnx_node.attribute.append(
            helper.make_attribute(
                "max",
                aidge_node.get_operator().max()
        ))
    return [onnx_node]
