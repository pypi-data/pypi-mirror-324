from typing import Tuple
import unittest
import funcnodes as fn
from sklearn.base import RegressorMixin, TransformerMixin

# from sklearn.cross_decomposition import CCA, PLSCanonical, PLSRegression
from funcnodes_sklearn.cross_decomposition import (
    cca,
    pls_canonical,
    Algorithm,
    pls_regression,
    pls_svd,
)


class TestCCA(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        X = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [2.0, 2.0, 2.0], [3.0, 5.0, 4.0]]
        Y = [[0.1, -0.2], [0.9, 1.1], [6.2, 5.9], [11.9, 12.3]]
        model: fn.Node = cca()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        cross_decomposition = out.value().fit(X, Y)
        transform = cross_decomposition.transform(X, Y)
        self.assertIsInstance(cross_decomposition, RegressorMixin)
        self.assertIsInstance(transform, Tuple)


class TestPLSCanonical(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        X = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [2.0, 2.0, 2.0], [3.0, 5.0, 4.0]]
        Y = [[0.1, -0.2], [0.9, 1.1], [6.2, 5.9], [11.9, 12.3]]
        model: fn.Node = pls_canonical()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        cross_decomposition = out.value().fit(X, Y)
        transform = cross_decomposition.transform(X, Y)
        self.assertIsInstance(cross_decomposition, RegressorMixin)
        self.assertIsInstance(transform, Tuple)

    async def test_custom_parameters(self):
        X = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [2.0, 2.0, 2.0], [3.0, 5.0, 4.0]]
        Y = [[0.1, -0.2], [0.9, 1.1], [6.2, 5.9], [11.9, 12.3]]
        algorithm = Algorithm.svd.value
        model: fn.Node = pls_canonical()
        model.inputs["algorithm"].value = algorithm
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        cross_decomposition = out.value().fit(X, Y)
        transform = cross_decomposition.transform(X, Y)
        self.assertIsInstance(cross_decomposition, RegressorMixin)
        self.assertIsInstance(transform, Tuple)


class TestPLSRegression(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        X = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [2.0, 2.0, 2.0], [3.0, 5.0, 4.0]]
        Y = [[0.1, -0.2], [0.9, 1.1], [6.2, 5.9], [11.9, 12.3]]
        model: fn.Node = pls_regression()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        cross_decomposition = out.value().fit(X, Y)
        transform = cross_decomposition.transform(X, Y)
        self.assertIsInstance(cross_decomposition, RegressorMixin)
        self.assertIsInstance(transform, Tuple)


class TestPLSSVD(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        X = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [2.0, 2.0, 2.0], [3.0, 5.0, 4.0]]
        Y = [[0.1, -0.2], [0.9, 1.1], [6.2, 5.9], [11.9, 12.3]]
        model: fn.Node = pls_svd()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        cross_decomposition = out.value().fit(X, Y)
        transform = cross_decomposition.transform(X, Y)
        self.assertIsInstance(cross_decomposition, TransformerMixin)
        self.assertIsInstance(transform, Tuple)
