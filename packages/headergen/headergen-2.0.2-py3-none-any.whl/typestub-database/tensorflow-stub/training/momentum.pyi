from tensorflow.python.framework import ops as ops
from tensorflow.python.ops import math_ops as math_ops
from tensorflow.python.training import optimizer as optimizer, training_ops as training_ops
from tensorflow.python.util.tf_export import tf_export as tf_export

class MomentumOptimizer(optimizer.Optimizer):
    def __init__(self, learning_rate, momentum, use_locking: bool = ..., name: str = ..., use_nesterov: bool = ...) -> None: ...
