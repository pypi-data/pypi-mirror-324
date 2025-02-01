import unittest
import funcnodes as fn

# from funcnodes_sklearn.preprocessing import (
#     _label_encoder,
#     _one_hot_encoder
# )
from sklearn.base import BaseEstimator
from funcnodes_sklearn.discriminant_analysis import _lda, _qda


class TestLDA(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        # model1: fn.Node = _lda()
        # self.assertIsInstance(model1, fn.Node)
        # model1.trigger()
        # await model1
        # X = model1.outputs["data"].value
        # n_components = 7
        # random_state = 0
        model: fn.Node = _lda()
        # model.inputs["n_components"].value = n_components
        # model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        # decomposition = out.value.fit_(X)
        # X_transformed = out.value().fit_transform(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        # self.assertEqual(X_transformed.shape, (1797, n_components))


class TestQDA(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        model: fn.Node = _qda()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        self.assertIsInstance(out.value(), BaseEstimator)
        # self.assertEqual(X_transformed.shape, (1797, n_components))
