from tensorflow.python.eager import context as context
from tensorflow.python.framework import ops as ops
from tensorflow.python.keras.utils.generic_utils import LazyLoader as LazyLoader
from typing import Any

training: Any
training_v1: Any
base_layer: Any
base_layer_v1: Any
callbacks: Any
callbacks_v1: Any

class ModelVersionSelector:
    def __new__(cls, *args, **kwargs): ...

class LayerVersionSelector:
    def __new__(cls, *args, **kwargs): ...

class TensorBoardVersionSelector:
    def __new__(cls, *args, **kwargs): ...

def should_use_v2(): ...
def swap_class(cls, v2_cls, v1_cls, use_v2): ...
def disallow_legacy_graph(cls_name, method_name) -> None: ...
def is_v1_layer_or_model(obj): ...
