import numpy as np
from scipy.sparse import csr_matrix
import unittest
import funcnodes as fn
from sklearn.base import BaseEstimator
from sklearn.datasets import (
    make_multilabel_classification,
    make_sparse_coded_signal,
    make_friedman1,
)
from funcnodes_sklearn.decomposition import (
    _dictionary_learning,
    TransformAlgorithm,
    _factor_analysis,
    _fast_ica,
    _incrementa_lpca,
    _kernel_lpca,
    _latent_dirichlet_allocation,
    _mini_batch_dictionary_learning,
    _mini_batch_sparse_pca,
    _nmf,
    Init,
    _mini_batch_nmf,
    _pca,
    _sparse_pca,
    _sparse_coder,
    _truncated_svd,
)
from funcnodes_sklearn.datasets import _digits


class TestDictionaryLearning(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        X, dictionary, code = make_sparse_coded_signal(
            n_samples=30,
            n_components=15,
            n_features=20,
            n_nonzero_coefs=10,
            random_state=42,
        )
        n_components = 15
        transform_algorithm = TransformAlgorithm.lasso_lars.value
        transform_alpha = 0.1
        random_state = 42
        model: fn.Node = _dictionary_learning()
        model.inputs["n_components"].value = n_components
        model.inputs["transform_algorithm"].value = transform_algorithm
        model.inputs["transform_alpha"].value = transform_alpha
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        decomposition = out.value().fit(X)
        X_transformed = decomposition.transform(X)
        self.assertIsInstance(decomposition, BaseEstimator)
        self.assertAlmostEqual(np.mean(X_transformed), 0.021422536390435117)


class TestFactorAnalysis(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        model1: fn.Node = _digits()
        self.assertIsInstance(model1, fn.Node)
        await model1
        X = model1.outputs["data"].value
        n_components = 7
        random_state = 0
        model: fn.Node = _factor_analysis()
        model.inputs["n_components"].value = n_components
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        # decomposition = out.value.fit_(X)
        X_transformed = out.value().fit_transform(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        self.assertEqual(X_transformed.shape, (1797, n_components))


class TestFastICA(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        model1: fn.Node = _digits()
        self.assertIsInstance(model1, fn.Node)
        await model1
        X = model1.outputs["data"].value
        n_components = 7
        random_state = 0
        # whiten='unit-variance'
        model: fn.Node = _fast_ica()
        model.inputs["n_components"].value = n_components
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        # decomposition = out.value.fit_(X)
        X_transformed = out.value().fit_transform(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        self.assertEqual(X_transformed.shape, (1797, n_components))


class TestIncrementalPCA(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        model1: fn.Node = _digits()
        self.assertIsInstance(model1, fn.Node)
        await model1
        X = model1.outputs["data"].value
        n_components = 7
        batch_size = 200
        # whiten='unit-variance'
        model: fn.Node = _incrementa_lpca()
        model.inputs["n_components"].value = n_components
        model.inputs["batch_size"].value = batch_size
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        # decomposition = out.value.fit_(X)
        X_transformed = out.value().fit_transform(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        self.assertEqual(X_transformed.shape, (1797, n_components))


class TestKernelPCA(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        model1: fn.Node = _digits()
        self.assertIsInstance(model1, fn.Node)
        await model1
        X = model1.outputs["data"].value
        n_components = 7
        kernel = "linear"
        model: fn.Node = _kernel_lpca()
        model.inputs["n_components"].value = n_components
        model.inputs["kernel"].value = kernel
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        # decomposition = out.value.fit_(X)
        X_transformed = out.value().fit_transform(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        self.assertEqual(X_transformed.shape, (1797, n_components))


class TestLatentDirichletAllocation(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        X, _ = make_multilabel_classification(random_state=0)
        n_components = 5
        random_state = 0
        model: fn.Node = _latent_dirichlet_allocation()
        model.inputs["n_components"].value = n_components
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        decomposition = out.value().fit(X)
        X_transformed = decomposition.transform(X[-2:])
        self.assertIsInstance(out.value(), BaseEstimator)
        self.assertEqual(X_transformed.shape, (2, n_components))


class TestMiniBatchDictionaryLearning(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        X, dictionary, code = make_sparse_coded_signal(
            n_samples=30,
            n_components=15,
            n_features=20,
            n_nonzero_coefs=10,
            random_state=42,
        )
        n_components = 15
        batch_size = 3
        transform_algorithm = TransformAlgorithm.lasso_lars.value
        transform_alpha = 0.1
        max_iter = 20
        random_state = 42
        model: fn.Node = _mini_batch_dictionary_learning()
        model.inputs["n_components"].value = n_components
        model.inputs["batch_size"].value = batch_size
        model.inputs["transform_algorithm"].value = transform_algorithm
        model.inputs["transform_alpha"].value = transform_alpha
        model.inputs["max_iter"].value = max_iter
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        X_transformed = out.value().fit_transform(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        self.assertTrue(np.mean(X_transformed == 0) > 0.0)


class TestMiniBatchSparsePCA(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        X, _ = make_friedman1(n_samples=200, n_features=30, random_state=0)
        n_components = 5
        batch_size = 50
        max_iter = 10
        random_state = 0
        model: fn.Node = _mini_batch_sparse_pca()
        model.inputs["n_components"].value = n_components
        model.inputs["batch_size"].value = batch_size
        model.inputs["max_iter"].value = max_iter
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        decomposition = out.value().fit(X)
        X_transformed = decomposition.transform(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        self.assertEqual(X_transformed.shape, (200, n_components))
        self.assertTrue(np.mean(decomposition.components_ == 0) > 0.5)


class TestNMF(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        X = np.array([[1, 1], [2, 1], [3, 1.2], [4, 1], [5, 0.8], [6, 1]])
        n_components = 2
        init = Init.random.value
        random_state = 0
        model: fn.Node = _nmf()
        model.inputs["n_components"].value = n_components
        model.inputs["init"].value = init
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        X_transformed = out.value().fit_transform(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        self.assertEqual(X_transformed.shape, (6, n_components))


class TestMiniBatchNMF(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        X = np.array([[1, 1], [2, 1], [3, 1.2], [4, 1], [5, 0.8], [6, 1]])
        n_components = 2
        init = Init.random.value
        random_state = 0
        model: fn.Node = _mini_batch_nmf()
        model.inputs["n_components"].value = n_components
        model.inputs["init"].value = init
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        X_transformed = out.value().fit_transform(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        self.assertEqual(X_transformed.shape, (6, n_components))


class TestPCA(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
        n_components = 2
        model: fn.Node = _pca()
        model.inputs["n_components"].value = n_components
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        decomposition = out.value().fit(X)
        # X_transformed = decomposition.transform(X)
        # X_transformed = out.value().fit_transform(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        # self.assertEqual(X_transformed.shape, (6, n_components))
        self.assertEqual(decomposition.components_.shape, (n_components, 2))


class TestSparsePCA(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        X, _ = make_friedman1(n_samples=200, n_features=30, random_state=0)
        n_components = 5
        random_state = 0
        model: fn.Node = _sparse_pca()
        model.inputs["n_components"].value = n_components
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        X_transformed = out.value().fit_transform(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        self.assertEqual(X_transformed.shape, (200, n_components))


class TestSparseCoder(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        X = np.array([[-1, -1, -1], [0, 0, 3]])
        dictionary = np.array(
            [[0, 1, 0], [-1, -1, 2], [1, 1, 1], [0, 1, 1], [0, 2, 1]], dtype=np.float64
        )
        dictionary = dictionary
        transform_algorithm = TransformAlgorithm.lasso_lars.value
        transform_alpha = 1e-10
        model: fn.Node = _sparse_coder()
        model.inputs["dictionary"].value = dictionary
        model.inputs["transform_algorithm"].value = transform_algorithm
        model.inputs["transform_alpha"].value = transform_alpha

        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        X_transformed = out.value().transform(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        np.testing.assert_array_almost_equal(
            X_transformed,
            [[0.0, 0.0, -1.0, 0.0, 0.0], [0.0, 1.0, 0.9999999999999999, 0.0, 0.0]],
        )


class TestTruncatedSVD(unittest.IsolatedAsyncioTestCase):
    async def test_parameters(self):
        np.random.seed(0)
        X_dense = np.random.rand(100, 100)
        X_dense[:, 2 * np.arange(50)] = 0
        X = csr_matrix(X_dense)
        n_components = 5
        n_iter = 7
        random_state = 42
        model: fn.Node = _truncated_svd()
        model.inputs["n_components"].value = n_components
        model.inputs["n_iter"].value = n_iter
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        decomposition = out.value().fit(X)
        self.assertIsInstance(out.value(), BaseEstimator)
        self.assertEqual(decomposition.components_.shape, (n_components, 100))
