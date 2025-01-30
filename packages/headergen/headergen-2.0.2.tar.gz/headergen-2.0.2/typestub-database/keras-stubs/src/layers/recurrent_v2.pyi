from typing import Any

from keras import activations as activations
from keras import backend as backend
from keras.src.engine import base_layer as base_layer
from keras.src.engine.input_spec import InputSpec as InputSpec
from keras.src.layers import recurrent as recurrent

class _DefunWrapper:
    time_major: Any
    go_backwards: Any
    layer_name: Any
    defun_layer: Any
    def __init__(self, time_major, go_backwards, layer_name) -> None: ...
    def __deepcopy__(self, memo): ...

class GRUCell(recurrent.GRUCell):
    def __init__(
        self,
        units,
        activation: str = ...,
        recurrent_activation: str = ...,
        use_bias: bool = ...,
        kernel_initializer: str = ...,
        recurrent_initializer: str = ...,
        bias_initializer: str = ...,
        kernel_regularizer: Any | None = ...,
        recurrent_regularizer: Any | None = ...,
        bias_regularizer: Any | None = ...,
        kernel_constraint: Any | None = ...,
        recurrent_constraint: Any | None = ...,
        bias_constraint: Any | None = ...,
        dropout: float = ...,
        recurrent_dropout: float = ...,
        reset_after: bool = ...,
        **kwargs
    ) -> None: ...

class GRU(recurrent.DropoutRNNCellMixin, recurrent.GRU, base_layer.BaseRandomLayer):
    def __init__(
        self,
        units,
        activation: str = ...,
        recurrent_activation: str = ...,
        use_bias: bool = ...,
        kernel_initializer: str = ...,
        recurrent_initializer: str = ...,
        bias_initializer: str = ...,
        kernel_regularizer: Any | None = ...,
        recurrent_regularizer: Any | None = ...,
        bias_regularizer: Any | None = ...,
        activity_regularizer: Any | None = ...,
        kernel_constraint: Any | None = ...,
        recurrent_constraint: Any | None = ...,
        bias_constraint: Any | None = ...,
        dropout: float = ...,
        recurrent_dropout: float = ...,
        return_sequences: bool = ...,
        return_state: bool = ...,
        go_backwards: bool = ...,
        stateful: bool = ...,
        unroll: bool = ...,
        time_major: bool = ...,
        reset_after: bool = ...,
        **kwargs
    ) -> None: ...
    def call(
        self,
        inputs,
        mask: Any | None = ...,
        training: Any | None = ...,
        initial_state: Any | None = ...,
    ): ...

def standard_gru(
    inputs,
    init_h,
    kernel,
    recurrent_kernel,
    bias,
    mask,
    time_major,
    go_backwards,
    sequence_lengths,
    zero_output_for_mask,
): ...
def gpu_gru(
    inputs,
    init_h,
    kernel,
    recurrent_kernel,
    bias,
    mask,
    time_major,
    go_backwards,
    sequence_lengths,
): ...
def gru_with_backend_selection(
    inputs,
    init_h,
    kernel,
    recurrent_kernel,
    bias,
    mask,
    time_major,
    go_backwards,
    sequence_lengths,
    zero_output_for_mask,
): ...

class LSTMCell(recurrent.LSTMCell):
    def __init__(
        self,
        units,
        activation: str = ...,
        recurrent_activation: str = ...,
        use_bias: bool = ...,
        kernel_initializer: str = ...,
        recurrent_initializer: str = ...,
        bias_initializer: str = ...,
        unit_forget_bias: bool = ...,
        kernel_regularizer: Any | None = ...,
        recurrent_regularizer: Any | None = ...,
        bias_regularizer: Any | None = ...,
        kernel_constraint: Any | None = ...,
        recurrent_constraint: Any | None = ...,
        bias_constraint: Any | None = ...,
        dropout: float = ...,
        recurrent_dropout: float = ...,
        **kwargs
    ) -> None: ...

class LSTM(recurrent.DropoutRNNCellMixin, recurrent.LSTM, base_layer.BaseRandomLayer):
    return_runtime: Any
    state_spec: Any
    def __init__(
        self,
        units,
        activation: str = ...,
        recurrent_activation: str = ...,
        use_bias: bool = ...,
        kernel_initializer: str = ...,
        recurrent_initializer: str = ...,
        bias_initializer: str = ...,
        unit_forget_bias: bool = ...,
        kernel_regularizer: Any | None = ...,
        recurrent_regularizer: Any | None = ...,
        bias_regularizer: Any | None = ...,
        activity_regularizer: Any | None = ...,
        kernel_constraint: Any | None = ...,
        recurrent_constraint: Any | None = ...,
        bias_constraint: Any | None = ...,
        dropout: float = ...,
        recurrent_dropout: float = ...,
        return_sequences: bool = ...,
        return_state: bool = ...,
        go_backwards: bool = ...,
        stateful: bool = ...,
        time_major: bool = ...,
        unroll: bool = ...,
        **kwargs
    ) -> None: ...
    def call(
        self,
        inputs,
        mask: Any | None = ...,
        training: Any | None = ...,
        initial_state: Any | None = ...,
    ): ...

def standard_lstm(
    inputs,
    init_h,
    init_c,
    kernel,
    recurrent_kernel,
    bias,
    mask,
    time_major,
    go_backwards,
    sequence_lengths,
    zero_output_for_mask,
): ...
def gpu_lstm(
    inputs,
    init_h,
    init_c,
    kernel,
    recurrent_kernel,
    bias,
    mask,
    time_major,
    go_backwards,
    sequence_lengths,
): ...
def lstm_with_backend_selection(
    inputs,
    init_h,
    init_c,
    kernel,
    recurrent_kernel,
    bias,
    mask,
    time_major,
    go_backwards,
    sequence_lengths,
    zero_output_for_mask,
): ...
def is_sequence_right_padded(mask): ...
def has_fully_masked_sequence(mask): ...
def is_cudnn_supported_inputs(mask, time_major): ...
def calculate_sequence_by_mask(mask, time_major): ...
