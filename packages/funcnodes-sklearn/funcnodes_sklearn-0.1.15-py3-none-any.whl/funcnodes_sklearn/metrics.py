from funcnodes import Shelf, NodeDecorator
from typing import Optional
import numpy as np
from enum import Enum
from sklearn.metrics import (
    # model selection interface
    confusion_matrix,
)


class Normalize(Enum):
    true = "true"
    pred = "pred"
    all = "all"
    NONE = None

    @classmethod
    def default(cls):
        return cls.NONE.value


@NodeDecorator(
    node_id="sklearn.metrics.confusion_matrix",
    name="confusion_matrix",
)
def _confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    labels: Optional[np.ndarray] = None,
    sample_weight: Optional[np.ndarray] = None,
    normalize: Normalize = Normalize.default(),
) -> np.ndarray:
    return confusion_matrix(
        y_true=y_true,
        y_pred=y_pred,
        labels=labels,
        sample_weight=sample_weight,
        normalize=normalize,
    )


CLASSIFICATION_NODE_SHELFE = Shelf(
    nodes=[_confusion_matrix],
    subshelves=[],
    name="Classification metrics",
    description="""The sklearn.metrics module implements several loss, score, and utility
    functions to measure classification performance. Some metrics might require probability estimates of the positive
    class, confidence values, or binary decisions values. Most implementations allow each sample to provide a weighted
    contribution to the overall score, through the sample_weight parameter.""",
)


METRICS_NODE_SHELFE = Shelf(
    nodes=[],
    subshelves=[CLASSIFICATION_NODE_SHELFE],
    name="Metrics",
    description="Score functions, performance metrics, pairwise metrics and distance computations.",
)
