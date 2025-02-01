from typing import Iterator, Tuple
import numpy as np
import unittest

# # from unittest.mock import patch, Mock, MagicMock
# from sklearn.covariance import (
#     EmpiricalCovariance,
#     EllipticEnvelope,
#     GraphicalLasso,
#     GraphicalLassoCV,
#     LedoitWolf,
#     MinCovDet,
#     OAS,
#     ShrunkCovariance,
# )
from funcnodes_sklearn.covariance import (
    empirical_covariance,
    elliptical_envelpoe,
    graphical_lasso,
    Mode,
    graphical_lasso_cv,
    ledoit_wolf,
    min_cov_det,
    oas,
    shrunk_covariance,
)

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import funcnodes as fn

X = np.array([[1, 1], [2, 1], [1, 0], [4, 7], [3, 5], [3, 6]])


class TestEmpiricalCovariance(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        cov: fn.Node = empirical_covariance()
        self.assertIsInstance(cov, fn.Node)

        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)

        np.testing.assert_array_almost_equal(
            model.covariance_,
            [
                [1.2222222222222223, 2.8888888888888893],
                [2.8888888888888893, 7.555555555555555],
            ],
        )

        np.testing.assert_array_almost_equal(
            model.location_,
            [2.3333333333333335, 3.3333333333333335],
        )


class TestEllipticEnvelope(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        cov: fn.Node = elliptical_envelpoe()
        self.assertIsInstance(cov, fn.Node)

        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)

        np.testing.assert_array_almost_equal(
            model.covariance_,
            [
                [1.2222222222222223, 2.8888888888888893],
                [2.8888888888888893, 7.555555555555555],
            ],
        )

        np.testing.assert_array_almost_equal(
            model.location_,
            [2.3333333333333335, 3.3333333333333335],
        )

    async def test_predict(self):
        cov: fn.Node = elliptical_envelpoe()
        cov.inputs["random_state"].value = 0
        self.assertIsInstance(cov, fn.Node)
        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)

        np.testing.assert_array_almost_equal(
            model.predict([[0, 0], [3, 3]]),
            [-1, -1],
        )


class TestGraphicalLasso(unittest.IsolatedAsyncioTestCase):
    true_cov = np.array(
        [
            [0.8, 0.0, 0.2, 0.0],
            [0.0, 0.4, 0.0, 0.0],
            [0.2, 0.0, 0.3, 0.1],
            [0.0, 0.0, 0.1, 0.7],
        ]
    )
    np.random.seed(0)
    X = np.random.multivariate_normal(mean=[0, 0, 0, 0], cov=true_cov, size=200)

    async def test_default_parameters(self):
        cov: fn.Node = graphical_lasso()
        self.assertIsInstance(cov, fn.Node)

        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)

        np.testing.assert_array_almost_equal(
            model.covariance_,
            [[1.222, 2.879], [2.879, 7.556]],
            decimal=3,
        )

        np.testing.assert_array_almost_equal(
            model.location_,
            [2.333, 3.333],
            decimal=3,
        )


class TestGraphicalLassoCV(unittest.IsolatedAsyncioTestCase):
    true_cov = np.array(
        [
            [0.8, 0.0, 0.2, 0.0],
            [0.0, 0.4, 0.0, 0.0],
            [0.2, 0.0, 0.3, 0.1],
            [0.0, 0.0, 0.1, 0.7],
        ]
    )
    np.random.seed(0)
    X = np.random.multivariate_normal(mean=[0, 0, 0, 0], cov=true_cov, size=200)

    async def test_default_parameters(self):
        cov: fn.Node = graphical_lasso_cv()
        self.assertIsInstance(cov, fn.Node)

        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)

        np.testing.assert_array_almost_equal(
            model.covariance_,
            [
                [1.222, 2.843],
                [2.843, 7.556],
            ],
            decimal=3,
        )

        np.testing.assert_array_almost_equal(
            model.location_,
            [2.3333333333333335, 3.3333333333333335],
        )

    async def test_custom_parameters(self):
        def generate_random_splits(
            num_splits: int, dataset_size: int, train_size: float = 0.8
        ) -> Iterator[Tuple[np.ndarray[int], np.ndarray[int]]]:
            for _ in range(num_splits):
                indices = np.random.permutation(dataset_size)
                train_indices = indices[: int(train_size * dataset_size)]
                test_indices = indices[int(train_size * dataset_size) :]
                yield train_indices, test_indices

        X, y = make_classification(
            n_samples=100, n_features=2, n_redundant=0, random_state=42
        )
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, train_size=0.8, random_state=42
        )
        num_splits = 2
        dataset_size = len(X)
        splits = generate_random_splits(num_splits, dataset_size)
        cov: fn.Node = graphical_lasso_cv()
        cov.inputs["mode"].value = Mode.lars.value
        cov.inputs["cv"].value = splits
        self.assertIsInstance(cov, fn.Node)
        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)

        np.testing.assert_array_almost_equal(
            model.location_,
            [-0.02771408348295842, -0.04884843210402259],
        )


class TestLedoitWolf(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        cov: fn.Node = ledoit_wolf()
        self.assertIsInstance(cov, fn.Node)

        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)

        np.testing.assert_array_almost_equal(
            model.covariance_,
            [
                [1.528977, 2.609042],
                [2.609042, 7.248801],
            ],
            decimal=3,
        )

        np.testing.assert_array_almost_equal(
            model.location_,
            [2.3333333333333335, 3.3333333333333335],
        )

    async def test_custom_parameters(self):
        cov: fn.Node = ledoit_wolf()
        cov.inputs["store_precision"].value = False
        cov.inputs["assume_centered"].value = True
        cov.inputs["block_size"].value = 1
        self.assertIsInstance(cov, fn.Node)
        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)

        np.testing.assert_array_almost_equal(
            model.covariance_,
            [[8.73, 6.99], [6.99, 16.6]],
            decimal=2,
        )

        np.testing.assert_array_almost_equal(
            model.location_,
            [0, 0],
        )


class TestMinCovDet(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        cov: fn.Node = min_cov_det()
        self.assertIsInstance(cov, fn.Node)

        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)

        np.testing.assert_array_almost_equal(
            model.covariance_,
            [
                [1.2222222222222223, 2.8888888888888893],
                [2.8888888888888893, 7.555555555555555],
            ],
        )

        np.testing.assert_array_almost_equal(
            model.location_,
            [2.3333333333333335, 3.3333333333333335],
        )

    async def test_custom_parameters(self):
        cov: fn.Node = min_cov_det()
        cov.inputs["random_state"].value = 0
        self.assertIsInstance(cov, fn.Node)
        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)

        np.testing.assert_array_almost_equal(
            model.location_,
            [2.3333333333333335, 3.3333333333333335],
        )

        print(model.covariance_)
        np.testing.assert_array_almost_equal(
            model.covariance_,
            [[1.22222222, 2.88888889], [2.88888889, 7.55555556]],
            decimal=2,
        )


class TestOAS(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        cov: fn.Node = oas()
        self.assertIsInstance(cov, fn.Node)

        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)

        np.testing.assert_array_almost_equal(
            model.covariance_,
            [[3.1, 1.18], [1.18, 5.68]],
            decimal=2,
        )


class TestShrunkCovariance(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        cov: fn.Node = shrunk_covariance()
        self.assertIsInstance(cov, fn.Node)

        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)
        np.testing.assert_array_almost_equal(
            model.covariance_,
            [[1.54, 2.6], [2.6, 7.24]],
            decimal=2,
        )

        np.testing.assert_array_almost_equal(
            model.location_,
            [2.33, 3.33],
            decimal=2,
        )

    async def test_custom_parameters(self):
        cov: fn.Node = shrunk_covariance()
        cov.inputs["shrinkage"].value = 0.5
        self.assertIsInstance(cov, fn.Node)
        await cov
        out = cov.outputs["out"]
        model = out.value()
        model.fit(X)

        np.testing.assert_array_almost_equal(
            model.covariance_,
            [[2.81, 1.44], [1.44, 5.97]],
            decimal=2,
        )

        np.testing.assert_array_almost_equal(
            model.location_,
            [2.33, 3.33],
            decimal=2,
        )
