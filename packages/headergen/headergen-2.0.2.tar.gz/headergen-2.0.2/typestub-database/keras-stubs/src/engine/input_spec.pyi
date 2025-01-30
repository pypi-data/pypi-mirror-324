from typing import Any

from keras import backend as backend

class InputSpec:
    dtype: Any
    ndim: Any
    shape: Any
    max_ndim: Any
    min_ndim: Any
    name: Any
    allow_last_axis_squeeze: Any
    axes: Any
    def __init__(
        self,
        dtype: Any | None = ...,
        shape: Any | None = ...,
        ndim: Any | None = ...,
        max_ndim: Any | None = ...,
        min_ndim: Any | None = ...,
        axes: Any | None = ...,
        allow_last_axis_squeeze: bool = ...,
        name: Any | None = ...,
    ) -> None: ...
    def get_config(self): ...
    @classmethod
    def from_config(cls, config): ...

def to_tensor_shape(spec): ...
def assert_input_compatibility(input_spec, inputs, layer_name) -> None: ...
def display_shape(shape): ...
def to_tensor_spec(input_spec, default_dtype: Any | None = ...): ...
