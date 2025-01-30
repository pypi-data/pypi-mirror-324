from typing import Any

import tensorflow.compat.v2 as tf
from keras import backend as backend

class Optimizer:
    updates: Any
    weights: Any
    def __init__(self, **kwargs) -> None: ...
    def get_updates(self, loss, params) -> None: ...
    def get_gradients(self, loss, params): ...
    def set_weights(self, weights) -> None: ...
    def get_weights(self): ...
    def get_config(self): ...
    @classmethod
    def from_config(cls, config): ...

class SGD(Optimizer):
    iterations: Any
    lr: Any
    momentum: Any
    decay: Any
    initial_decay: Any
    nesterov: Any
    def __init__(
        self,
        lr: float = ...,
        momentum: float = ...,
        decay: float = ...,
        nesterov: bool = ...,
        **kwargs
    ) -> None: ...
    updates: Any
    def get_updates(self, loss, params): ...
    def get_config(self): ...

class RMSprop(Optimizer):
    lr: Any
    rho: Any
    decay: Any
    iterations: Any
    epsilon: Any
    initial_decay: Any
    def __init__(
        self,
        lr: float = ...,
        rho: float = ...,
        epsilon: Any | None = ...,
        decay: float = ...,
        **kwargs
    ) -> None: ...
    updates: Any
    def get_updates(self, loss, params): ...
    def get_config(self): ...

class Adagrad(Optimizer):
    lr: Any
    decay: Any
    iterations: Any
    epsilon: Any
    initial_decay: Any
    def __init__(
        self, lr: float = ..., epsilon: Any | None = ..., decay: float = ..., **kwargs
    ) -> None: ...
    updates: Any
    def get_updates(self, loss, params): ...
    def get_config(self): ...

class Adadelta(Optimizer):
    lr: Any
    decay: Any
    iterations: Any
    rho: Any
    epsilon: Any
    initial_decay: Any
    def __init__(
        self,
        lr: float = ...,
        rho: float = ...,
        epsilon: Any | None = ...,
        decay: float = ...,
        **kwargs
    ) -> None: ...
    updates: Any
    def get_updates(self, loss, params): ...
    def get_config(self): ...

class Adam(Optimizer):
    iterations: Any
    lr: Any
    beta_1: Any
    beta_2: Any
    decay: Any
    epsilon: Any
    initial_decay: Any
    amsgrad: Any
    def __init__(
        self,
        lr: float = ...,
        beta_1: float = ...,
        beta_2: float = ...,
        epsilon: Any | None = ...,
        decay: float = ...,
        amsgrad: bool = ...,
        **kwargs
    ) -> None: ...
    updates: Any
    def get_updates(self, loss, params): ...
    def get_config(self): ...

class Adamax(Optimizer):
    iterations: Any
    lr: Any
    beta_1: Any
    beta_2: Any
    decay: Any
    epsilon: Any
    initial_decay: Any
    def __init__(
        self,
        lr: float = ...,
        beta_1: float = ...,
        beta_2: float = ...,
        epsilon: Any | None = ...,
        decay: float = ...,
        **kwargs
    ) -> None: ...
    updates: Any
    def get_updates(self, loss, params): ...
    def get_config(self): ...

class Nadam(Optimizer):
    iterations: Any
    m_schedule: Any
    lr: Any
    beta_1: Any
    beta_2: Any
    epsilon: Any
    schedule_decay: Any
    def __init__(
        self,
        lr: float = ...,
        beta_1: float = ...,
        beta_2: float = ...,
        epsilon: Any | None = ...,
        schedule_decay: float = ...,
        **kwargs
    ) -> None: ...
    updates: Any
    def get_updates(self, loss, params): ...
    def get_config(self): ...

class TFOptimizer(Optimizer, tf.__internal__.tracking.Trackable):
    optimizer: Any
    iterations: Any
    def __init__(self, optimizer, iterations: Any | None = ...) -> None: ...
    def minimize(
        self, loss, var_list, grad_loss: Any | None = ..., tape: Any | None = ...
    ) -> None: ...
    def apply_gradients(self, grads_and_vars) -> None: ...
    def get_grads(self, loss, params): ...
    updates: Any
    def get_updates(self, loss, params): ...
    @property
    def weights(self) -> None: ...
    def get_config(self) -> None: ...
    def from_config(self, config) -> None: ...

sgd = SGD
rmsprop = RMSprop
adagrad = Adagrad
adadelta = Adadelta
adam = Adam
adamax = Adamax
nadam = Nadam
