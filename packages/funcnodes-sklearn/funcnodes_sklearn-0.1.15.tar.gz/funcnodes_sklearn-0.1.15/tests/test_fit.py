import unittest
import funcnodes as fn
import numpy as np
from funcnodes_sklearn.preprocessing import (
    _label_encoder,
    _one_hot_encoder,
)

from funcnodes_sklearn.discriminant_analysis import (
    _lda,
)

from funcnodes_sklearn.fit import (
    _fit,
    _inverse_transform,
    _transform,
    _predict,
)


class TestFittingingNodes(unittest.IsolatedAsyncioTestCase):
    async def test_fit_transform_one_hot_encoder(self):
        model: fn.Node = _one_hot_encoder()
        self.assertIsInstance(model, fn.Node)
        X = [["Male", 1], ["Female", 3], ["Female", 2]]

        # async def test_fit(self):
        ft_model: fn.Node = _fit()
        ft_model.inputs["model"].connect(model.outputs["out"])
        ft_model.inputs["X"].value = X
        self.assertIsInstance(ft_model, fn.Node)
        # await fn.run_until_complete(ft_model,model)
        # print(ft_model.outputs["out"])

        X_t = [["Female", 1], ["Male", 4]]
        t_model: fn.Node = _transform()
        t_model.inputs["model"].connect(ft_model.outputs["out"])
        t_model.inputs["X"].value = X_t
        self.assertIsInstance(t_model, fn.Node)

        await fn.run_until_complete(t_model, ft_model, model)
        out = t_model.outputs["out"]
        np.testing.assert_array_equal(
            out.value, [[1.0, 0.0, 1.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0, 0.0]]
        )

    async def test_fit_inverse_transform_one_hot_encoder(self):
        model: fn.Node = _one_hot_encoder()
        self.assertIsInstance(model, fn.Node)
        X = [["Male", 1], ["Female", 3], ["Female", 2]]

        # async def test_fit(self):
        ft_model: fn.Node = _fit()
        ft_model.inputs["model"].connect(model.outputs["out"])
        ft_model.inputs["X"].value = X
        self.assertIsInstance(ft_model, fn.Node)

        X_it = [[0, 1, 1, 0, 0], [0, 0, 0, 1, 0]]
        it_model = _inverse_transform()
        it_model.inputs["model"].connect(ft_model.outputs["out"])
        it_model.inputs["X"].value = X_it
        self.assertIsInstance(it_model, fn.Node)

        await fn.run_until_complete(it_model, ft_model, model)
        out = it_model.outputs["out"]
        np.testing.assert_array_equal(out.value, [["Male", 1], [None, 2]])

    async def test_fit_transform_label_encoder(self):
        model: fn.Node = _label_encoder()
        self.assertIsInstance(model, fn.Node)
        X = [1, 2, 2, 6]

        # async def test_fit(self):
        ft_model: fn.Node = _fit()
        ft_model.inputs["model"].connect(model.outputs["out"])
        ft_model.inputs["X"].value = X
        self.assertIsInstance(ft_model, fn.Node)
        # await fn.run_until_complete(ft_model,model)
        # print(ft_model.outputs["out"])

        X_t = [1, 1, 2, 6]
        t_model: fn.Node = _transform()
        t_model.inputs["model"].connect(ft_model.outputs["out"])
        t_model.inputs["X"].value = X_t
        self.assertIsInstance(t_model, fn.Node)

        await fn.run_until_complete(t_model, ft_model, model)
        out = t_model.outputs["out"]
        np.testing.assert_array_equal(out.value, [0, 0, 1, 2])

    async def test_fit_inverse_transform_label_encoder(self):
        model: fn.Node = _label_encoder()
        self.assertIsInstance(model, fn.Node)
        X = [1, 2, 2, 6]

        # async def test_fit(self):
        ft_model: fn.Node = _fit()
        ft_model.inputs["model"].connect(model.outputs["out"])
        ft_model.inputs["X"].value = X
        self.assertIsInstance(ft_model, fn.Node)

        X_it = [0, 0, 1, 2]
        it_model = _inverse_transform()
        it_model.inputs["model"].connect(ft_model.outputs["out"])
        it_model.inputs["X"].value = X_it
        self.assertIsInstance(it_model, fn.Node)

        await fn.run_until_complete(it_model, ft_model, model)
        out = it_model.outputs["out"]
        np.testing.assert_array_equal(out.value, [1, 1, 2, 6])

    async def test_fit_predict(self):
        model: fn.Node = _lda()
        self.assertIsInstance(model, fn.Node)
        X = [[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]]
        y = [1, 1, 1, 2, 2, 2]

        # async def test_fit(self):
        ft_model: fn.Node = _fit()
        ft_model.inputs["model"].connect(model.outputs["out"])

        ft_model.inputs["X"].value = X
        ft_model.inputs["y"].value = y

        self.assertIsInstance(ft_model, fn.Node)
        # await fn.run_until_complete(ft_model,model)
        # print(ft_model.outputs["out"])

        X_p = [[-0.8, -1]]
        p_model: fn.Node = _predict()
        p_model.inputs["model"].connect(ft_model.outputs["out"])
        p_model.inputs["X"].value = X_p

        self.assertIsInstance(p_model, fn.Node)

        await fn.run_until_complete(p_model, ft_model, model)
        out = p_model.outputs["out"]
        np.testing.assert_array_equal(out.value, [1])
