import sys
import os
from typing import List
import unittest
import funcnodes as fn
import funcnodes_sklearn as fnmodule  # noqa

sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)  # in case test folder is not in sys path
from all_nodes_test_base import TestAllNodesBase  # noqa: E402

fn.config.IN_NODE_TEST = True

from test_calibration import TestCalibratedClassifierCV, TestCalibrationCurve  # noqa: E402
from test_cluster import (  # noqa: E402
    TestAffinityPropagation,
    TestAgglomerativeClustering,
    TestBirchFunction,
    TestDBSCAN,
    TestFeatureAgglomeration,
    TestKMeans,
    TestBisectingKMeans,
    TestMiniBatchKMeans,
    TestMeanShift,
    TestOPTICS,
    TestSpectralClustering,
    TestSpectralBiclustering,
    TestSpectralCoclustering,
)

from test_covariance import (  # noqa: E402
    TestEmpiricalCovariance,
    TestEllipticEnvelope,
    TestGraphicalLasso,
    TestGraphicalLassoCV,
    TestLedoitWolf,
    TestMinCovDet,
    TestOAS,
    TestShrunkCovariance,
)

from test_cross_decomposition import (  # noqa: E402
    TestCCA,
    TestPLSCanonical,
    TestPLSRegression,
    TestPLSSVD,
)

from test_decomposition import (  # noqa: E402
    TestDictionaryLearning,
    TestFactorAnalysis,
    TestFastICA,
    TestIncrementalPCA,
    TestKernelPCA,
    TestLatentDirichletAllocation,
    TestMiniBatchDictionaryLearning,
    TestMiniBatchSparsePCA,
    TestMiniBatchNMF,
    TestNMF,
    TestPCA,
    TestSparsePCA,
    TestSparseCoder,
    TestTruncatedSVD,
)

from test_discriminant_analysis import (  # noqa: E402
    TestLDA,
    TestQDA,
)

from test_fit import (  # noqa: E402
    TestFittingingNodes,
)

from test_metrics import (  # noqa: E402
    TestMetrics,
)

from test_preprocessing import (  # noqa: E402
    TestPreprocessingNodes,
)


class TestAllNodes(TestAllNodesBase):
    # in this test class all nodes should be triggered at least once to mark them as testing

    # if you tests your nodes with in other test classes, add them here
    # this will automtically extend this test class with the tests in the other test classes
    # but this will also mean if you run all tests these tests might run multiple times
    # also the correspondinig setups and teardowns will not be called, so the tests should be
    # independently callable
    sub_test_classes: List[unittest.IsolatedAsyncioTestCase] = [
        TestCalibratedClassifierCV,
        TestCalibrationCurve,
        TestAffinityPropagation,
        TestAgglomerativeClustering,
        TestBirchFunction,
        TestDBSCAN,
        TestFeatureAgglomeration,
        TestKMeans,
        TestBisectingKMeans,
        TestMiniBatchKMeans,
        TestMeanShift,
        TestOPTICS,
        TestSpectralClustering,
        TestSpectralBiclustering,
        TestSpectralCoclustering,
        TestEmpiricalCovariance,
        TestEllipticEnvelope,
        TestGraphicalLasso,
        TestGraphicalLassoCV,
        TestLedoitWolf,
        TestMinCovDet,
        TestOAS,
        TestShrunkCovariance,
        TestCCA,
        TestPLSCanonical,
        TestPLSRegression,
        TestPLSSVD,
        TestDictionaryLearning,
        TestFactorAnalysis,
        TestFastICA,
        TestMiniBatchNMF,
        TestSparseCoder,
        TestIncrementalPCA,
        TestKernelPCA,
        TestLatentDirichletAllocation,
        TestMiniBatchDictionaryLearning,
        TestMiniBatchSparsePCA,
        TestNMF,
        TestPCA,
        TestSparsePCA,
        TestTruncatedSVD,
        TestLDA,
        TestQDA,
        TestFittingingNodes,
        TestMetrics,
        TestPreprocessingNodes,
    ]

    # if you have specific nodes you dont want to test, add them here
    # But why would you do that, it will ruin the coverage?!
    # a specific use case would be ignore nodes that e.g. load a lot of data, but there we would recommend
    # to write tests with patches and not ignore them.
    ignore_nodes: List[fn.Node] = (
        [] + fn.flatten_shelf(fnmodule.datasets.DATASET_NODE_SHELF)[0]
    )
