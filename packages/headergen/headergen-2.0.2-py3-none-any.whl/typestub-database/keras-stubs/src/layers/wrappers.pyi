from typing import Any

from keras import backend as backend
from keras.src.engine.base_layer import Layer as Layer
from keras.src.engine.input_spec import InputSpec as InputSpec
from keras.utils import generic_utils as generic_utils
from keras.utils import layer_utils as layer_utils
from keras.utils import tf_inspect as tf_inspect
from keras.utils import tf_utils as tf_utils

class Wrapper(Layer):
    layer: Any
    def __init__(self, layer, **kwargs) -> None: ...
    built: bool
    def build(self, input_shape: Any | None = ...) -> None: ...
    @property
    def activity_regularizer(self): ...
    def get_config(self): ...
    @classmethod
    def from_config(cls, config, custom_objects: Any | None = ...): ...

class TimeDistributed(Wrapper):
    supports_masking: bool
    def __init__(self, layer, **kwargs) -> None: ...
    input_spec: Any
    built: bool
    def build(self, input_shape): ...
    def compute_output_shape(self, input_shape): ...
    def call(self, inputs, training: Any | None = ..., mask: Any | None = ...): ...
    def compute_mask(self, inputs, mask: Any | None = ...): ...

class Bidirectional(Wrapper):
    forward_layer: Any
    backward_layer: Any
    merge_mode: Any
    stateful: Any
    return_sequences: Any
    return_state: Any
    supports_masking: bool
    input_spec: Any
    def __init__(
        self,
        layer,
        merge_mode: str = ...,
        weights: Any | None = ...,
        backward_layer: Any | None = ...,
        **kwargs
    ) -> None: ...
    def compute_output_shape(self, input_shape): ...
    def __call__(
        self,
        inputs,
        initial_state: Any | None = ...,
        constants: Any | None = ...,
        **kwargs
    ): ...
    def call(
        self,
        inputs,
        training: Any | None = ...,
        mask: Any | None = ...,
        initial_state: Any | None = ...,
        constants: Any | None = ...,
    ): ...
    def reset_states(self) -> None: ...
    built: bool
    def build(self, input_shape) -> None: ...
    def compute_mask(self, inputs, mask): ...
    @property
    def constraints(self): ...
    def get_config(self): ...
    @classmethod
    def from_config(cls, config, custom_objects: Any | None = ...): ...
