from typing import Any

from keras import backend as backend
from keras.src.engine import training_utils as training_utils
from keras.src.engine import training_utils_v1 as training_utils_v1
from keras.utils import data_utils as data_utils
from keras.utils import generic_utils as generic_utils
from keras.utils.mode_keys import ModeKeys as ModeKeys

def model_iteration(
    model,
    data,
    steps_per_epoch: Any | None = ...,
    epochs: int = ...,
    verbose: int = ...,
    callbacks: Any | None = ...,
    validation_data: Any | None = ...,
    validation_steps: Any | None = ...,
    validation_freq: int = ...,
    class_weight: Any | None = ...,
    max_queue_size: int = ...,
    workers: int = ...,
    use_multiprocessing: bool = ...,
    shuffle: bool = ...,
    initial_epoch: int = ...,
    mode=...,
    batch_size: Any | None = ...,
    steps_name: str = ...,
    **kwargs
): ...

fit_generator: Any
evaluate_generator: Any
predict_generator: Any

def convert_to_generator_like(
    data,
    batch_size: Any | None = ...,
    steps_per_epoch: Any | None = ...,
    epochs: int = ...,
    shuffle: bool = ...,
): ...

class GeneratorOrSequenceTrainingLoop(training_utils_v1.TrainingLoop):
    def fit(
        self,
        model,
        x: Any | None = ...,
        y: Any | None = ...,
        batch_size: Any | None = ...,
        epochs: int = ...,
        verbose: int = ...,
        callbacks: Any | None = ...,
        validation_split: float = ...,
        validation_data: Any | None = ...,
        shuffle: bool = ...,
        class_weight: Any | None = ...,
        sample_weight: Any | None = ...,
        initial_epoch: int = ...,
        steps_per_epoch: Any | None = ...,
        validation_steps: Any | None = ...,
        validation_freq: int = ...,
        max_queue_size: int = ...,
        workers: int = ...,
        use_multiprocessing: bool = ...,
    ): ...
    def evaluate(
        self,
        model,
        x: Any | None = ...,
        y: Any | None = ...,
        batch_size: Any | None = ...,
        verbose: int = ...,
        sample_weight: Any | None = ...,
        steps: Any | None = ...,
        callbacks: Any | None = ...,
        max_queue_size: int = ...,
        workers: int = ...,
        use_multiprocessing: bool = ...,
    ): ...
    def predict(
        self,
        model,
        x,
        batch_size: Any | None = ...,
        verbose: int = ...,
        steps: Any | None = ...,
        callbacks: Any | None = ...,
        max_queue_size: int = ...,
        workers: int = ...,
        use_multiprocessing: bool = ...,
    ): ...

class EagerDatasetOrIteratorTrainingLoop(training_utils_v1.TrainingLoop):
    def fit(
        self,
        model,
        x: Any | None = ...,
        y: Any | None = ...,
        batch_size: Any | None = ...,
        epochs: int = ...,
        verbose: int = ...,
        callbacks: Any | None = ...,
        validation_split: float = ...,
        validation_data: Any | None = ...,
        shuffle: bool = ...,
        class_weight: Any | None = ...,
        sample_weight: Any | None = ...,
        initial_epoch: int = ...,
        steps_per_epoch: Any | None = ...,
        validation_steps: Any | None = ...,
        validation_freq: int = ...,
        **kwargs
    ): ...
    def evaluate(
        self,
        model,
        x: Any | None = ...,
        y: Any | None = ...,
        batch_size: Any | None = ...,
        verbose: int = ...,
        sample_weight: Any | None = ...,
        steps: Any | None = ...,
        callbacks: Any | None = ...,
        **kwargs
    ): ...
    def predict(
        self,
        model,
        x,
        batch_size: Any | None = ...,
        verbose: int = ...,
        steps: Any | None = ...,
        callbacks: Any | None = ...,
        **kwargs
    ): ...

class GeneratorLikeTrainingLoop(training_utils_v1.TrainingLoop):
    def fit(
        self,
        model,
        x: Any | None = ...,
        y: Any | None = ...,
        batch_size: Any | None = ...,
        epochs: int = ...,
        verbose: int = ...,
        callbacks: Any | None = ...,
        validation_split: float = ...,
        validation_data: Any | None = ...,
        shuffle: bool = ...,
        class_weight: Any | None = ...,
        sample_weight: Any | None = ...,
        initial_epoch: int = ...,
        steps_per_epoch: Any | None = ...,
        validation_steps: Any | None = ...,
        validation_freq: int = ...,
        **kwargs
    ): ...
    def evaluate(
        self,
        model,
        x: Any | None = ...,
        y: Any | None = ...,
        batch_size: Any | None = ...,
        verbose: int = ...,
        sample_weight: Any | None = ...,
        steps: Any | None = ...,
        callbacks: Any | None = ...,
        **kwargs
    ): ...
    def predict(
        self,
        model,
        x,
        batch_size: Any | None = ...,
        verbose: int = ...,
        steps: Any | None = ...,
        callbacks: Any | None = ...,
        **kwargs
    ): ...
