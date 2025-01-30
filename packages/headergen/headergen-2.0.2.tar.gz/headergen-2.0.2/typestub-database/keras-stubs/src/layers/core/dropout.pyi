from typing import Any

from keras import backend as backend
from keras.src.engine import base_layer as base_layer
from keras.utils import control_flow_util as control_flow_util

class Dropout(base_layer.BaseRandomLayer):
    rate: Any
    noise_shape: Any
    seed: Any
    supports_masking: bool
    def __init__(
        self, rate, noise_shape: Any | None = ..., seed: Any | None = ..., **kwargs
    ) -> None: ...
    def build(self, input_shape) -> None: ...
    def call(self, inputs, training: Any | None = ...): ...
    def compute_output_shape(self, input_shape): ...
    def get_config(self): ...
