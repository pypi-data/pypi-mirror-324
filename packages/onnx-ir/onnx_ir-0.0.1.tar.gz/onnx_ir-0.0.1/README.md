# ONNX IR

> [!NOTE]
> This is an adaptation of the `onnxscript.ir` module from the ONNX Script project: https://github.com/microsoft/onnxscript/tree/main/onnxscript/ir

An in-memory IR that supports the full ONNX spec, designed for graph construction, analysis and transformation.

## Features ✨

- Full ONNX spec support: all valid models representable by ONNX protobuf, and a subset of invalid models (so you can load and fix them).
- Low memory footprint: mmap'ed external tensors; unified interface for ONNX TensorProto, Numpy arrays and PyTorch Tensors etc. No tensor size limitation. Zero copies.
- Straightforward access patterns: Access value information and traverse the graph topology at ease.
- Robust mutation: Create as many iterators as you like on the graph while mutating it.
- Speed: Performant graph manipulation, serialization/deserialization to Protobuf.
- Pythonic and familiar APIs: Classes define Pythonic apis and still map to ONNX protobuf concepts in an intuitive way.
- No protobuf dependency: The IR does not require protobuf once the model is converted to the IR representation, decoupling from the serialization format.

## Code Organization 🗺️

- [`_protocols.py`](_protocols.py): Interfaces defined for all entities in the IR.
- [`_core.py`](_core.py): Implementation of the core entities in the IR, including `Model`, `Graph`, `Node`, `Value`, and others.
- [`_enums.py`](_enums.py): Definition of the type enums that correspond to the `DataType` and `AttributeType` in `onnx.proto`.
- [`_name_authority.py`](_name_authority.py): The authority for giving names to entities in the graph, used internally.
- [`_linked_list.py`](_linked_list.py): The data structure as the node container in the graph that supports robust iteration and mutation. Internal.
- [`_metadata.py`](_metadata.py): Metadata store for all entities in the IR.
