import unittest
from sklearn.datasets import make_classification
from sklearn.base import ClassifierMixin
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from funcnodes_sklearn.calibration import (
    calibrated_classifier_cv,
    calibrationcurve,
    Method,
    Strategy,
)

from typing import Iterator, Tuple
import numpy as np
import funcnodes as fn


def generate_random_splits(
    num_splits: int, dataset_size: int, train_size: float = 0.8
) -> Iterator[Tuple[np.ndarray[int], np.ndarray[int]]]:
    for _ in range(num_splits):
        indices = np.random.permutation(dataset_size)
        train_indices = indices[: int(train_size * dataset_size)]
        test_indices = indices[int(train_size * dataset_size) :]
        yield train_indices, test_indices


class TestCalibratedClassifierCV(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        calibrated_clf: fn.Node = calibrated_classifier_cv()
        self.assertIsInstance(calibrated_clf, fn.Node)

        await calibrated_clf
        out = calibrated_clf.outputs["out"]
        model = out.value()
        X, y = make_classification(
            n_samples=100, n_features=2, n_redundant=0, random_state=42
        )
        self.assertIsInstance(out, fn.NodeOutput)
        self.assertIsInstance(model, ClassifierMixin)
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        self.assertEqual(len(model.calibrated_classifiers_), 5)
        self.assertGreater(accuracy_score(y_test, y_pred), 0.5)

    async def test_integer_cv(self):
        _cv = 3
        calibrated_clf: fn.Node = calibrated_classifier_cv()
        calibrated_clf.inputs["cv"].value = _cv
        calibrated_clf.inputs["estimator"].value = GaussianNB()
        self.assertIsInstance(calibrated_clf, fn.Node)
        await calibrated_clf
        out = calibrated_clf.outputs["out"]
        model = out.value()
        X, y = make_classification(
            n_samples=100, n_features=2, n_redundant=0, random_state=42
        )
        self.assertIsInstance(out, fn.NodeOutput)
        self.assertIsInstance(model, ClassifierMixin)
        model.fit(X, y)
        self.assertEqual(len(model.calibrated_classifiers_), _cv)

        np.testing.assert_array_almost_equal(
            model.predict_proba(X)[:5, :],
            [
                [0.09961242910399655, 0.9003875708960035],
                [0.0, 1.0],
                [1.0, 0.0],
                [1.0, 0.0],
                [0.0, 1.0],
            ],
        )

    async def test_string_cv(self):
        X, y = make_classification(
            n_samples=100, n_features=2, n_redundant=0, random_state=42
        )
        X_train, X_calib, y_train, y_calib = train_test_split(X, y, random_state=42)
        _cv = "prefit"
        base_clf = GaussianNB()

        calibrated_clf: fn.Node = calibrated_classifier_cv()
        calibrated_clf.inputs["cv"].value = _cv
        calibrated_clf.inputs["estimator"].value = base_clf.fit(X_train, y_train)
        self.assertIsInstance(calibrated_clf, fn.Node)
        await calibrated_clf
        out = calibrated_clf.outputs["out"]
        model = out.value()

        self.assertIsInstance(out, fn.NodeOutput)
        self.assertIsInstance(model, ClassifierMixin)
        model.fit(X_calib, y_calib)
        self.assertEqual(len(model.calibrated_classifiers_), 1)

        np.testing.assert_almost_equal(model.predict_proba([[-0.5, 0.5]]), [[1.0, 0.0]])

    async def test_isotonic_calibration(self):
        calibrated_clf: fn.Node = calibrated_classifier_cv()
        calibrated_clf.inputs["method"].value = Method.isotonic.value
        self.assertIsInstance(calibrated_clf, fn.Node)
        await calibrated_clf
        out = calibrated_clf.outputs["out"]
        model = out.value()
        X, y = make_classification(
            n_samples=100, n_features=2, n_redundant=0, random_state=42
        )
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
        self.assertIsInstance(out, fn.NodeOutput)
        self.assertIsInstance(model, ClassifierMixin)
        model.fit(X, y)
        y_pred = model.predict(X_test)
        self.assertEqual(len(model.calibrated_classifiers_), 5)
        self.assertGreater(accuracy_score(y_test, y_pred), 0.5)


class TestCalibrationCurve(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        y_true = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1])
        y_prob = np.array([0.1, 0.2, 0.3, 0.4, 0.65, 0.7, 0.8, 0.9, 1.0])
        calibrated_clf: fn.Node = calibrationcurve()
        calibrated_clf.inputs["y_true"].value = y_true
        calibrated_clf.inputs["y_prob"].value = y_prob
        self.assertIsInstance(calibrated_clf, fn.Node)
        await calibrated_clf
        prob_true = calibrated_clf.outputs["prob_true"].value
        prob_pred = calibrated_clf.outputs["prob_pred"].value
        self.assertIsInstance(prob_true, np.ndarray)
        self.assertIsInstance(prob_pred, np.ndarray)

    async def test_custom_parameters(self):
        y_true = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1])
        y_prob = np.array([0.1, 0.2, 0.3, 0.4, 0.65, 0.7, 0.8, 0.9, 1.0])
        calibrated_clf: fn.Node = calibrationcurve()
        calibrated_clf.inputs["y_true"].value = y_true
        calibrated_clf.inputs["y_prob"].value = y_prob
        calibrated_clf.inputs["strategy"].value = Strategy.quantile.value
        calibrated_clf.inputs["n_bins"].value = 3
        calibrated_clf.inputs["pos_label"].value = 1.1
        self.assertIsInstance(calibrated_clf, fn.Node)
        await calibrated_clf
        prob_true = calibrated_clf.outputs["prob_true"].value
        prob_pred = calibrated_clf.outputs["prob_pred"].value
        self.assertIsInstance(prob_true, np.ndarray)
        self.assertIsInstance(prob_pred, np.ndarray)
