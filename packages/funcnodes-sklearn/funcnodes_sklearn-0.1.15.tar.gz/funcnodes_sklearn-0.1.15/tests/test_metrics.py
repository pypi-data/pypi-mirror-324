import unittest
import funcnodes as fn
import numpy as np
from funcnodes_sklearn.metrics import (
    _confusion_matrix,
)


class TestMetrics(unittest.IsolatedAsyncioTestCase):
    async def test_confusion_matrix(self):
        y_true = [2, 0, 2, 2, 0, 1]
        y_pred = [0, 0, 2, 2, 0, 2]
        metric: fn.Node = _confusion_matrix()
        metric.inputs["y_true"].value = y_true
        metric.inputs["y_pred"].value = y_pred
        self.assertIsInstance(metric, fn.Node)
        await metric
        out = metric.outputs["out"]
        np.testing.assert_array_equal(out.value, [[2, 0, 0], [0, 0, 1], [1, 0, 2]])
