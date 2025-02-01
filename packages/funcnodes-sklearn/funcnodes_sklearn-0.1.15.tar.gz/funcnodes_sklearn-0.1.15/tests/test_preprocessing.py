import unittest
import funcnodes as fn
from sklearn.base import BaseEstimator
from funcnodes_sklearn.preprocessing import (
    _binarizer,
    _function_transformer,
    _kbins_discretizer,
    _kbins_centerer,
    _label_binarizer,
    _label_encoder,
    _max_abs_scaler,
    _min_max_scaler,
    _multi_label_binarizer,
    _normalizer,
    _one_hot_encoder,
    _ordinal_encoder,
    _polynomial_features,
    _power_transformer,
    _quantile_transformer,
    _robust_scaler,
    _standard_scaler,
    _target_encoder,
)


class TestPreprocessingNodes(unittest.IsolatedAsyncioTestCase):
    # async def test_default_parameters(self):
    #     tests = [
    #         _binarizer,
    #         _function_transformer,
    #         _kbins_discretizer,
    #         _kbins_centerer,
    #         _label_binarizer,
    #         _label_encoder,
    #         _max_abs_scaler,
    #         _min_max_scaler,
    #         _normalizer,
    #         _one_hot_encoder,
    #         _ordinal_encoder,
    #         _polynomial_features,
    #         _power_transformer,
    #         _quantile_transformer,
    #         _robust_scaler,
    #         _standard_scaler
    #     ]

    #     for test in tests:
    #         model: fn.Node = test()
    #         self.assertIsInstance(model, fn.Node)
    #         await model
    #         out = model.outputs["out"]
    #         pp = out.value()
    #         self.assertIsInstance(pp, BaseEstimator)

    async def test_binarizer(self):
        model: fn.Node = _binarizer()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_function_transformer(self):
        model: fn.Node = _function_transformer()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_kbins_discretizer(self):
        model: fn.Node = _kbins_discretizer()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_kbins_centerer(self):
        model: fn.Node = _kbins_centerer()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_label_binarizer(self):
        model: fn.Node = _label_binarizer()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_label_encoder(self):
        model: fn.Node = _label_encoder()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_max_abs_scaler(self):
        model: fn.Node = _max_abs_scaler()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_min_max_scaler(self):
        model: fn.Node = _min_max_scaler()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_normalizer(self):
        model: fn.Node = _normalizer()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_one_hot_encoder(self):
        model: fn.Node = _one_hot_encoder()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_ordinal_encoder(self):
        model: fn.Node = _ordinal_encoder()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_polynomial_features(self):
        model: fn.Node = _polynomial_features()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_power_transformer(self):
        model: fn.Node = _power_transformer()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_quantile_transformer(self):
        model: fn.Node = _quantile_transformer()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_robust_scaler(self):
        model: fn.Node = _robust_scaler()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_standard_scaler(self):
        model: fn.Node = _standard_scaler()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_multi_label_binarizer(self):
        model: fn.Node = _multi_label_binarizer()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)

    async def test_target_encoder(self):
        model: fn.Node = _target_encoder()
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        pp = out.value()
        self.assertIsInstance(pp, BaseEstimator)


# if __name__ == "__main__":
#     unittest.main()
