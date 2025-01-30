import abc
from typing import Any, List, Tuple, Union

from keras import activations as activations
from keras import backend as backend
from keras.losses import binary_crossentropy as binary_crossentropy
from keras.losses import categorical_crossentropy as categorical_crossentropy
from keras.losses import categorical_hinge as categorical_hinge
from keras.losses import hinge as hinge
from keras.losses import kullback_leibler_divergence as kullback_leibler_divergence
from keras.losses import logcosh as logcosh
from keras.losses import mean_absolute_error as mean_absolute_error
from keras.losses import (
    mean_absolute_percentage_error as mean_absolute_percentage_error,
)
from keras.losses import mean_squared_error as mean_squared_error
from keras.losses import (
    mean_squared_logarithmic_error as mean_squared_logarithmic_error,
)
from keras.losses import poisson as poisson
from keras.losses import (
    sparse_categorical_crossentropy as sparse_categorical_crossentropy,
)
from keras.losses import squared_hinge as squared_hinge
from keras.src.engine import base_layer as base_layer
from keras.src.engine import base_layer_utils as base_layer_utils
from keras.src.engine import keras_tensor as keras_tensor
from keras.src.saving.saved_model import metric_serialization as metric_serialization
from keras.utils import generic_utils as generic_utils
from keras.utils import losses_utils as losses_utils
from keras.utils import metrics_utils as metrics_utils
from keras.utils.generic_utils import (
    deserialize_keras_object as deserialize_keras_object,
)
from keras.utils.generic_utils import serialize_keras_object as serialize_keras_object
from keras.utils.generic_utils import to_list as to_list
from keras.utils.tf_utils import is_tensor_or_variable as is_tensor_or_variable

class Metric(base_layer.Layer, metaclass=abc.ABCMeta):
    stateful: bool
    built: bool
    def __init__(
        self, name: Any | None = ..., dtype: Any | None = ..., **kwargs
    ) -> None: ...
    def __new__(cls, *args, **kwargs): ...
    def __call__(self, *args, **kwargs): ...
    @property
    def dtype(self): ...
    def get_config(self): ...
    def reset_state(self): ...
    @abc.abstractmethod
    def update_state(self, *args, **kwargs): ...
    def merge_state(self, metrics): ...
    @abc.abstractmethod
    def result(self): ...
    def add_weight(
        self,
        name,
        shape=...,
        aggregation=...,
        synchronization=...,
        initializer: Any | None = ...,
        dtype: Any | None = ...,
    ): ...
    @property
    def trainable_weights(self): ...
    @property
    def non_trainable_weights(self): ...
    def reset_states(self): ...

class Reduce(Metric):
    reduction: Any
    total: Any
    count: Any
    def __init__(self, reduction, name, dtype: Any | None = ...) -> None: ...
    def update_state(self, values, sample_weight: Any | None = ...): ...
    def result(self): ...

class Sum(Reduce):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class Mean(Reduce):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class MeanRelativeError(Mean):
    normalizer: Any
    def __init__(
        self, normalizer, name: Any | None = ..., dtype: Any | None = ...
    ) -> None: ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...
    def get_config(self): ...

class MeanMetricWrapper(Mean):
    def __init__(
        self, fn, name: Any | None = ..., dtype: Any | None = ..., **kwargs
    ) -> None: ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...
    def get_config(self): ...
    @classmethod
    def from_config(cls, config): ...

class Accuracy(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class BinaryAccuracy(MeanMetricWrapper):
    def __init__(
        self, name: str = ..., dtype: Any | None = ..., threshold: float = ...
    ) -> None: ...

class CategoricalAccuracy(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class SparseCategoricalAccuracy(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class TopKCategoricalAccuracy(MeanMetricWrapper):
    def __init__(
        self, k: int = ..., name: str = ..., dtype: Any | None = ...
    ) -> None: ...

class SparseTopKCategoricalAccuracy(MeanMetricWrapper):
    def __init__(
        self, k: int = ..., name: str = ..., dtype: Any | None = ...
    ) -> None: ...

class _ConfusionMatrixConditionCount(Metric):
    init_thresholds: Any
    thresholds: Any
    accumulator: Any
    def __init__(
        self,
        confusion_matrix_cond,
        thresholds: Any | None = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...
    def result(self): ...
    def reset_state(self) -> None: ...
    def get_config(self): ...

class FalsePositives(_ConfusionMatrixConditionCount):
    def __init__(
        self,
        thresholds: Any | None = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...

class FalseNegatives(_ConfusionMatrixConditionCount):
    def __init__(
        self,
        thresholds: Any | None = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...

class TrueNegatives(_ConfusionMatrixConditionCount):
    def __init__(
        self,
        thresholds: Any | None = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...

class TruePositives(_ConfusionMatrixConditionCount):
    def __init__(
        self,
        thresholds: Any | None = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...

class Precision(Metric):
    init_thresholds: Any
    top_k: Any
    class_id: Any
    thresholds: Any
    true_positives: Any
    false_positives: Any
    def __init__(
        self,
        thresholds: Any | None = ...,
        top_k: Any | None = ...,
        class_id: Any | None = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...
    def result(self): ...
    def reset_state(self) -> None: ...
    def get_config(self): ...

class Recall(Metric):
    init_thresholds: Any
    top_k: Any
    class_id: Any
    thresholds: Any
    true_positives: Any
    false_negatives: Any
    def __init__(
        self,
        thresholds: Any | None = ...,
        top_k: Any | None = ...,
        class_id: Any | None = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...
    def result(self): ...
    def reset_state(self) -> None: ...
    def get_config(self): ...

class SensitivitySpecificityBase(Metric, metaclass=abc.ABCMeta):
    value: Any
    class_id: Any
    true_positives: Any
    true_negatives: Any
    false_positives: Any
    false_negatives: Any
    thresholds: Any
    def __init__(
        self,
        value,
        num_thresholds: int = ...,
        class_id: Any | None = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...
    def reset_state(self) -> None: ...
    def get_config(self): ...

class SensitivityAtSpecificity(SensitivitySpecificityBase):
    specificity: Any
    num_thresholds: Any
    def __init__(
        self,
        specificity,
        num_thresholds: int = ...,
        class_id: Any | None = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...
    def result(self): ...
    def get_config(self): ...

class SpecificityAtSensitivity(SensitivitySpecificityBase):
    sensitivity: Any
    num_thresholds: Any
    def __init__(
        self,
        sensitivity,
        num_thresholds: int = ...,
        class_id: Any | None = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...
    def result(self): ...
    def get_config(self): ...

class PrecisionAtRecall(SensitivitySpecificityBase):
    recall: Any
    num_thresholds: Any
    def __init__(
        self,
        recall,
        num_thresholds: int = ...,
        class_id: Any | None = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...
    def result(self): ...
    def get_config(self): ...

class RecallAtPrecision(SensitivitySpecificityBase):
    precision: Any
    num_thresholds: Any
    def __init__(
        self,
        precision,
        num_thresholds: int = ...,
        class_id: Any | None = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...
    def result(self): ...
    def get_config(self): ...

class AUC(Metric):
    num_thresholds: Any
    curve: Any
    summation_method: Any
    multi_label: Any
    label_weights: Any
    def __init__(
        self,
        num_thresholds: int = ...,
        curve: str = ...,
        summation_method: str = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
        thresholds: Any | None = ...,
        multi_label: bool = ...,
        num_labels: Any | None = ...,
        label_weights: Any | None = ...,
        from_logits: bool = ...,
    ) -> None: ...
    @property
    def thresholds(self): ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...
    def interpolate_pr_auc(self): ...
    def result(self): ...
    def reset_state(self) -> None: ...
    def get_config(self): ...

class CosineSimilarity(MeanMetricWrapper):
    def __init__(
        self, name: str = ..., dtype: Any | None = ..., axis: int = ...
    ) -> None: ...

class MeanAbsoluteError(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class MeanAbsolutePercentageError(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class MeanSquaredError(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class MeanSquaredLogarithmicError(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class Hinge(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class SquaredHinge(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class CategoricalHinge(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class RootMeanSquaredError(Mean):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...
    def result(self): ...

class LogCoshError(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class Poisson(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class KLDivergence(MeanMetricWrapper):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class _IoUBase(Metric, metaclass=abc.ABCMeta):
    num_classes: Any
    total_cm: Any
    def __init__(
        self, num_classes, name: Any | None = ..., dtype: Any | None = ...
    ) -> None: ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...
    def reset_state(self) -> None: ...

class IoU(_IoUBase):
    target_class_ids: Any
    def __init__(
        self,
        num_classes: int,
        target_class_ids: Union[List[int], Tuple[int, ...]],
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...
    def result(self): ...
    def get_config(self): ...

class BinaryIoU(IoU):
    threshold: Any
    def __init__(
        self,
        target_class_ids: Union[List[int], Tuple[int, ...]] = ...,
        threshold: float = ...,
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...
    def get_config(self): ...

class MeanIoU(IoU):
    def __init__(
        self, num_classes, name: Any | None = ..., dtype: Any | None = ...
    ) -> None: ...
    def get_config(self): ...

class OneHotIoU(IoU):
    def __init__(
        self,
        num_classes: int,
        target_class_ids: Union[List[int], Tuple[int, ...]],
        name: Any | None = ...,
        dtype: Any | None = ...,
    ) -> None: ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...

class OneHotMeanIoU(MeanIoU):
    def __init__(
        self, num_classes: int, name: Any | None = ..., dtype: Any | None = ...
    ) -> None: ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...

class MeanTensor(Metric):
    def __init__(
        self, name: str = ..., dtype: Any | None = ..., shape: Any | None = ...
    ) -> None: ...
    @property
    def total(self): ...
    @property
    def count(self): ...
    def update_state(self, values, sample_weight: Any | None = ...): ...
    def result(self): ...
    def reset_state(self) -> None: ...

class BinaryCrossentropy(MeanMetricWrapper):
    def __init__(
        self,
        name: str = ...,
        dtype: Any | None = ...,
        from_logits: bool = ...,
        label_smoothing: int = ...,
    ) -> None: ...

class CategoricalCrossentropy(MeanMetricWrapper):
    def __init__(
        self,
        name: str = ...,
        dtype: Any | None = ...,
        from_logits: bool = ...,
        label_smoothing: int = ...,
    ) -> None: ...

class SparseCategoricalCrossentropy(MeanMetricWrapper):
    def __init__(
        self,
        name: str = ...,
        dtype: Any | None = ...,
        from_logits: bool = ...,
        axis: int = ...,
    ) -> None: ...

class SumOverBatchSize(Reduce):
    def __init__(self, name: str = ..., dtype: Any | None = ...) -> None: ...

class SumOverBatchSizeMetricWrapper(SumOverBatchSize):
    def __init__(
        self, fn, name: Any | None = ..., dtype: Any | None = ..., **kwargs
    ) -> None: ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...): ...
    def get_config(self): ...

def accuracy(y_true, y_pred): ...
def binary_accuracy(y_true, y_pred, threshold: float = ...): ...
def categorical_accuracy(y_true, y_pred): ...
def sparse_categorical_accuracy(y_true, y_pred): ...
def top_k_categorical_accuracy(y_true, y_pred, k: int = ...): ...
def sparse_top_k_categorical_accuracy(y_true, y_pred, k: int = ...): ...
def cosine_proximity(y_true, y_pred, axis: int = ...): ...

acc = accuracy
ACC = accuracy
bce = binary_crossentropy
BCE = binary_crossentropy
mse = mean_squared_error
MSE = mean_squared_error
mae = mean_absolute_error
MAE = mean_absolute_error
mape = mean_absolute_percentage_error
MAPE = mean_absolute_percentage_error
msle = mean_squared_logarithmic_error
MSLE = mean_squared_logarithmic_error
cosine_similarity = cosine_proximity
log_cosh = logcosh

def clone_metric(metric): ...
def clone_metrics(metrics): ...
def serialize(metric): ...
def deserialize(config, custom_objects: Any | None = ...): ...
def get(identifier): ...
def is_built_in(cls): ...
