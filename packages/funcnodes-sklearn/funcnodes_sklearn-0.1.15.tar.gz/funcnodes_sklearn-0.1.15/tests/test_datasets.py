import unittest
import numpy as np
from pandas.core.frame import DataFrame
from pandas import Series
from scipy.sparse import spmatrix

from funcnodes_pandas import to_dict

import funcnodes as fn

# from typing import Tuple,
from funcnodes_sklearn.datasets import (
    _20newsgroups,
    _20newsgroups_vectorized,
    _20newsgroups_vectorized_as_frame,
    _california_housing,
    _california_housing_as_frame,
    _covtype,
    _covtype_as_frame,
    _kddcup99,
    _kddcup99_as_frame,
    _lfw_pairs,
    _lfw_people,
    _olivetti_faces,
    # _openml,
    _rcv1,
    # _species_distributions,
    _breast_cancer,
    _breast_cancer_as_frame,
    _diabetes,
    _diabetes_as_frame,
    _digits,
    # _digits_as_frame,
    # # _text_files,
    _iris,
    _iris_as_frame,
    _linnerud,
    _linnerud_as_frame,
    _sample_image,
    # # _svmlight_file
    _wine,
    _wine_as_frame,
    _biclusters,
    _blobs,
    _checkerboard,
    _circles,
    _classification,
    _friedman1,
    _friedman2,
    _friedman3,
    _gaussian_quantiles,
    _hastie_10_2,
    _low_rank_matrix,
    _moons,
    _multilabel_classification,
    _regression,
    _s_curve,
    _sparse_coded_signal,
    _sparse_spd_matrix,
    _sparse_uncorrelated,
    _spd_matrix,
    _swiss_roll,
)
import os
import tempfile
from _setup_env import config


KEEPDATA = config("KEEPDATA", default=False, cast=bool)


class DatasetsTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # assert scikit-learn loads the dataset to a temporary directory
        self.tempdir = tempfile.TemporaryDirectory()
        if not KEEPDATA:
            os.environ["SCIKIT_LEARN_DATA"] = self.tempdir.name

    def tearDown(self):
        self.tempdir.cleanup()


class Test20newsgroups(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _20newsgroups()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        DESCR = model.outputs["DESCR"].value
        target_names = model.outputs["target_names"].value
        self.assertIsInstance(data, list)
        self.assertIsInstance(target, np.ndarray)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(target_names, list)


class Test20newsgroupsVectorized(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _20newsgroups_vectorized()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        DESCR = model.outputs["DESCR"].value
        target_names = model.outputs["target_names"].value
        self.assertIsInstance(data, spmatrix)
        self.assertIsInstance(target, np.ndarray)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(target_names, list)


class Test20newsgroupsVectorizedAsFrame(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _20newsgroups_vectorized_as_frame()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        DESCR = model.outputs["DESCR"].value
        target_names = model.outputs["target_names"].value
        self.assertIsInstance(data, DataFrame)
        self.assertIsInstance(target, Series)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(target_names, list)


class TestCaliforniaHousing(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _california_housing()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        DESCR = model.outputs["DESCR"].value
        target_names = model.outputs["target_names"].value
        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(target, np.ndarray)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(target_names, list)


class TestCaliforniaHousingAsFrame(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _california_housing_as_frame()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        DESCR = model.outputs["DESCR"].value
        target_names = model.outputs["target_names"].value
        self.assertIsInstance(data, DataFrame)
        self.assertIsInstance(target, Series)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(target_names, list)


class TestCovtype(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _covtype()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        DESCR = model.outputs["DESCR"].value
        target_names = model.outputs["target_names"].value
        feature_names = model.outputs["feature_names"].value
        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(target, np.ndarray)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(target_names, list)
        self.assertIsInstance(feature_names, list)


class TestCovtypeAsFrame(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _covtype_as_frame()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        DESCR = model.outputs["DESCR"].value
        target_names = model.outputs["target_names"].value
        feature_names = model.outputs["feature_names"].value
        self.assertIsInstance(data, DataFrame)
        self.assertIsInstance(target, Series)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(target_names, list)
        self.assertIsInstance(feature_names, list)

    async def test_to_dict(self):
        model: fn.Node = _covtype_as_frame()

        todictnode = to_dict()

        model.outputs["data"].connect(todictnode.inputs["df"])

        await fn.run_until_complete(model, todictnode)

        self.assertIsInstance(todictnode.outputs["dict"].value, dict)


class TestKddcup99(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _kddcup99()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        DESCR = model.outputs["DESCR"].value
        target_names = model.outputs["target_names"].value
        feature_names = model.outputs["feature_names"].value
        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(target, np.ndarray)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(target_names, list)
        self.assertIsInstance(feature_names, list)


class TestKddcup99AsFrame(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _kddcup99_as_frame()
        self.assertIsInstance(model, fn.Node)
        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        DESCR = model.outputs["DESCR"].value
        target_names = model.outputs["target_names"].value
        feature_names = model.outputs["feature_names"].value
        self.assertIsInstance(data, DataFrame)
        self.assertIsInstance(target, Series)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(target_names, list)
        self.assertIsInstance(feature_names, list)


class TestLfwPairs(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _lfw_pairs()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        pairs = model.outputs["pairs"].value
        target = model.outputs["target"].value
        target_names = model.outputs["target_names"].value
        DESCR = model.outputs["DESCR"].value
        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(pairs, np.ndarray)
        self.assertIsInstance(target, np.ndarray)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(target_names, np.ndarray)


class TestLfwPeople(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _lfw_people()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        images = model.outputs["images"].value
        target = model.outputs["target"].value
        target_names = model.outputs["target_names"].value
        DESCR = model.outputs["DESCR"].value
        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(images, np.ndarray)
        self.assertIsInstance(target, np.ndarray)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(target_names, np.ndarray)


class TestOlivettiFaces(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _olivetti_faces()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        images = model.outputs["images"].value
        target = model.outputs["target"].value
        DESCR = model.outputs["DESCR"].value
        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(images, np.ndarray)
        self.assertIsInstance(target, np.ndarray)
        self.assertIsInstance(DESCR, str)


# class TestOpenml(DatasetsTestCase):
#     def test_default_parameters(self):
#         dataset = _openml()
#         self.assertIsInstance(dataset, dict)
#         # self.assertEqual(
#         #     list(dataset.keys()),
#         #     ["data", "target", "frame", "target_names", "feature_names", "DESCR"],
#         # )
class TestRcv1(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _rcv1()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        sample_id = model.outputs["sample_id"].value
        target = model.outputs["target"].value
        target_names = model.outputs["target_names"].value
        DESCR = model.outputs["DESCR"].value
        self.assertIsInstance(data, spmatrix)
        self.assertIsInstance(target, spmatrix)
        self.assertIsInstance(sample_id, np.ndarray)
        self.assertIsInstance(target_names, np.ndarray)
        self.assertIsInstance(DESCR, str)


# class TestSpeciesDistributions(DatasetsTestCase):
#     async def test_default_parameters(self):
#         model: fn.Node = _species_distributions()
#         self.assertIsInstance(model, fn.Node)
#
#         await model
#         coverages = model.outputs["coverages"].value
#         train = model.outputs["train"].value
#         test = model.outputs["test"].value
#         Nx = model.outputs["Nx"].value
#         Ny = model.outputs["Ny"].value
#         x_left_lower_corner = model.outputs["x_left_lower_corner"].value
#         y_left_lower_corner = model.outputs["y_left_lower_corner"].value
#         grid_size = model.outputs["grid_size"].value
#         # self.assertIsInstance(coverages, np.ndarray) # TODO: check if this is a np.array
#         # self.assertIsInstance(train, np.ndarray) # TODO: check if this is a np.array
#         # self.assertIsInstance(test, np.ndarray) # TODO: check if this is a np.array
#         self.assertIsInstance(Nx, int)
#         self.assertIsInstance(Ny, int)
#         self.assertIsInstance(x_left_lower_corner, float)
#         self.assertIsInstance(y_left_lower_corner, float)
#         self.assertIsInstance(grid_size, float)


class TestBreastCancer(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _breast_cancer()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        feature_names = model.outputs["feature_names"].value
        target_names = model.outputs["target_names"].value
        DESCR = model.outputs["DESCR"].value
        filename = model.outputs["filename"].value

        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(target, np.ndarray)
        self.assertIsInstance(feature_names, np.ndarray)
        self.assertIsInstance(target_names, np.ndarray)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(filename, str)


class TestBreastCancerAsFrame(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _breast_cancer_as_frame()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        feature_names = model.outputs["feature_names"].value
        target_names = model.outputs["target_names"].value
        DESCR = model.outputs["DESCR"].value
        filename = model.outputs["filename"].value

        self.assertIsInstance(data, DataFrame)
        self.assertIsInstance(target, Series)
        self.assertIsInstance(feature_names, np.ndarray)
        self.assertIsInstance(target_names, np.ndarray)
        self.assertIsInstance(DESCR, str)
        self.assertIsInstance(filename, str)


class TestDiabetes(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _diabetes()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value

        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(target, np.ndarray)


class TestDiabetesAsFrame(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _diabetes_as_frame()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value

        self.assertIsInstance(data, DataFrame)
        self.assertIsInstance(target, Series)


class TestDigits(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _digits()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(target, np.ndarray)


class TestDigitsAsFrame(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _diabetes_as_frame()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        self.assertIsInstance(data, DataFrame)
        self.assertIsInstance(target, Series)


# # class TestTextFiles(DatasetsTestCase):
# #     def test_default_parameters(self):
# #         dataset = _text_files()
# #         self.assertIsInstance(dataset, dict)


class TestIris(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _iris()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(target, np.ndarray)


class TestIrisAsFrame(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _iris_as_frame()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        self.assertIsInstance(data, DataFrame)
        self.assertIsInstance(target, Series)


class TestLinnerud(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _linnerud()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(target, np.ndarray)


class TestLinnerudAsFrame(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _linnerud_as_frame()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        self.assertIsInstance(data, DataFrame)
        self.assertIsInstance(target, DataFrame)


class TestSampleImage(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _sample_image()
        self.assertIsInstance(model, fn.Node)

        await model
        img = model.outputs["out"].value
        self.assertIsInstance(img, np.ndarray)
        self.assertEqual(img.shape, (427, 640, 3))


# # class TestSVMFile(DatasetsTestCase):
# #     def test_default_parameters(self):
# #         dataset = _svmlight_file()
# #         self.assertIsInstance(dataset, Tuple)


class TestWine(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _wine()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(target, np.ndarray)


class TestWineAsFrame(DatasetsTestCase):
    async def test_default_parameters(self):
        model: fn.Node = _wine_as_frame()
        self.assertIsInstance(model, fn.Node)

        await model
        data = model.outputs["data"].value
        target = model.outputs["target"].value
        self.assertIsInstance(data, DataFrame)
        self.assertIsInstance(target, Series)


# TODO: Fix test resulting in <NoValue>
class TestBiClusters(DatasetsTestCase):
    async def test_default_parameters(self):
        shape = (300, 300)
        n_clusters = 5
        noise = 5
        shuffle = False
        random_state = 0
        model: fn.Node = _biclusters()
        model.inputs["shape"].value = shape
        model.inputs["n_clusters"].value = n_clusters
        model.inputs["noise"].value = noise
        model.inputs["shuffle"].value = shuffle
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        rows = model.outputs["rows"].value
        cols = model.outputs["cols"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(rows, np.ndarray)
        self.assertIsInstance(cols, np.ndarray)


class TestBlobs(DatasetsTestCase):
    async def test_default_parameters(self):
        n_samples = 10
        centers = 3
        n_features = 2
        random_state = 0
        model: fn.Node = _blobs()
        model.inputs["n_samples"].value = n_samples
        model.inputs["centers"].value = centers
        model.inputs["n_features"].value = n_features
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        y = model.outputs["y"].value
        center = model.outputs["center"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)
        self.assertIsInstance(center, np.ndarray)


class TestCheckerboard(DatasetsTestCase):
    async def test_default_parameters(self):
        shape = (300, 300)
        n_clusters = (4, 3)
        noise = 10
        shuffle = False
        random_state = 42
        model: fn.Node = _checkerboard()
        model.inputs["shape"].value = shape
        model.inputs["n_clusters"].value = n_clusters
        model.inputs["noise"].value = noise
        model.inputs["shuffle"].value = shuffle
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        rows = model.outputs["rows"].value
        cols = model.outputs["cols"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(rows, np.ndarray)
        self.assertIsInstance(cols, np.ndarray)


class TestCircles(DatasetsTestCase):
    async def test_default_parameters(self):
        random_state = 42
        model: fn.Node = _circles()
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        y = model.outputs["y"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)


class TestClassification(DatasetsTestCase):
    async def test_default_parameters(self):
        random_state = 42
        model: fn.Node = _classification()
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        y = model.outputs["y"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)


class TestFriedman1(DatasetsTestCase):
    async def test_default_parameters(self):
        random_state = 42
        model: fn.Node = _friedman1()
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        y = model.outputs["y"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)


class TestFriedman2(DatasetsTestCase):
    async def test_default_parameters(self):
        random_state = 42
        model: fn.Node = _friedman2()
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        y = model.outputs["y"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)


class TestFriedman3(DatasetsTestCase):
    async def test_default_parameters(self):
        random_state = 42
        model: fn.Node = _friedman3()
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        y = model.outputs["y"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)


class TestGaussianQuantiles(DatasetsTestCase):
    async def test_default_parameters(self):
        random_state = 42
        model: fn.Node = _gaussian_quantiles()
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        y = model.outputs["y"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)


class TestHastie102(DatasetsTestCase):
    async def test_default_parameters(self):
        random_state = 1
        model: fn.Node = _hastie_10_2()
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        y = model.outputs["y"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)


class TestLowRankMatrix(DatasetsTestCase):
    async def test_default_parameters(self):
        n_samples, n_features = 500, 10
        random_state = np.random.RandomState(0)
        model: fn.Node = _low_rank_matrix()
        model.inputs["n_samples"].value = n_samples
        model.inputs["n_features"].value = n_features
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        self.assertIsInstance(X, np.ndarray)


class TestMoons(DatasetsTestCase):
    async def test_default_parameters(self):
        noise = 0.3
        random_state = 0
        model: fn.Node = _moons()
        model.inputs["noise"].value = noise
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        y = model.outputs["y"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)


class TestMultilabelClassification(DatasetsTestCase):
    async def test_default_parameters(self):
        n_labels = 5
        random_state = 42
        model: fn.Node = _multilabel_classification()
        model.inputs["n_labels"].value = n_labels
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        Y = model.outputs["Y"].value
        p_c = model.outputs["p_c"].value
        p_w_c = model.outputs["p_w_c"].value

        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(Y, np.ndarray)
        self.assertIsInstance(p_c, np.ndarray)
        self.assertIsInstance(p_w_c, np.ndarray)


class TestRegression(DatasetsTestCase):
    async def test_default_parameters(self):
        n_samples = 5
        n_features = 2
        noise = 1
        random_state = 42
        model: fn.Node = _regression()
        model.inputs["n_samples"].value = n_samples
        model.inputs["n_features"].value = n_features
        model.inputs["noise"].value = noise
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        y = model.outputs["y"].value
        coefs = model.outputs["coefs"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)
        self.assertIsInstance(coefs, np.ndarray)


class TestSCurve(DatasetsTestCase):
    async def test_default_parameters(self):
        n_samples = 1500
        random_state = 0
        model: fn.Node = _s_curve()
        model.inputs["n_samples"].value = n_samples
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        t = model.outputs["t"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(t, np.ndarray)


class TestSparseCodedSignal(DatasetsTestCase):
    async def test_default_parameters(self):
        n_samples = 1
        n_components, n_features = 512, 100
        n_nonzero_coefs = 17
        random_state = 0
        model: fn.Node = _sparse_coded_signal()
        model.inputs["n_samples"].value = n_samples
        model.inputs["n_components"].value = n_components
        model.inputs["n_features"].value = n_features
        model.inputs["n_nonzero_coefs"].value = n_nonzero_coefs
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        data = model.outputs["data"].value
        dictionary = model.outputs["dictionary"].value
        code = model.outputs["code"].value
        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(dictionary, np.ndarray)
        self.assertIsInstance(code, np.ndarray)


class TestSparseSpdMatrix(DatasetsTestCase):
    async def test_default_parameters(self):
        n_dim = 4
        norm_diag = False
        random_state = 42
        model: fn.Node = _sparse_spd_matrix()
        model.inputs["n_dim"].value = n_dim
        model.inputs["norm_diag"].value = norm_diag
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        prec = model.outputs["prec"].value
        self.assertIsInstance(prec, np.ndarray)


class TestSparseUncorrelated(DatasetsTestCase):
    async def test_default_parameters(self):
        random_state = 0
        model: fn.Node = _sparse_uncorrelated()
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        y = model.outputs["y"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)


class TestSpdMatrix(DatasetsTestCase):
    async def test_default_parameters(self):
        n_dim = 2
        random_state = 42
        model: fn.Node = _spd_matrix()
        model.inputs["n_dim"].value = n_dim
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        self.assertIsInstance(X, np.ndarray)


class TestSwissRoll(DatasetsTestCase):
    async def test_default_parameters(self):
        random_state = 0
        model: fn.Node = _swiss_roll()
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        X = model.outputs["X"].value
        t = model.outputs["t"].value
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(t, np.ndarray)
