import numpy as np
import unittest
import funcnodes as fn
from sklearn.base import ClusterMixin, BaseEstimator
from funcnodes_sklearn.cluster import (
    affinity_propagation,
    Affinity,
    agglomerative_clustering,
    Metric,
    Linkage,
    birch,
    dbscan,
    Algorithm,
    kmeans,
    KMeansAlgorithm,
    feature_agglomeration,
    bisecting_kmeans,
    BisectingStrategy,
    mini_batch_kmeans,
    mean_shift,
    optics,
    spectral_clustering,
    AssignLabels,
    spectral_biclustering,
    spectral_coclustering,
)
from joblib import Memory


class TestAffinityPropagation(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        model: fn.Node = affinity_propagation()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.damping, 0.5)
        self.assertEqual(clustering.max_iter, 200)
        self.assertEqual(clustering.convergence_iter, 15)
        self.assertTrue(clustering.copy)
        self.assertIsNone(clustering.preference)
        self.assertEqual(clustering.affinity, Affinity.default())
        self.assertFalse(clustering.verbose)
        self.assertIsNone(clustering.random_state)

    async def test_custom_parameters(self):
        damping = 0.7
        max_iter = 300
        convergence_iter = 20
        copy = False
        preference = np.array([0.1, 0.2, 0.3])
        affinity = Affinity.precomputed.value
        verbose = True
        random_state = 42
        model: fn.Node = affinity_propagation()
        model.inputs["damping"].value = damping
        model.inputs["max_iter"].value = max_iter
        model.inputs["convergence_iter"].value = convergence_iter
        model.inputs["copy"].value = copy
        model.inputs["preference"].value = preference
        model.inputs["affinity"].value = affinity
        model.inputs["verbose"].value = verbose
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.damping, damping)
        self.assertEqual(clustering.max_iter, max_iter)
        self.assertEqual(clustering.convergence_iter, convergence_iter)
        self.assertFalse(clustering.copy)
        np.testing.assert_array_equal(clustering.preference, preference)
        self.assertEqual(clustering.affinity, Affinity.precomputed.value)
        self.assertTrue(clustering.verbose)
        self.assertEqual(clustering.random_state, random_state)


class TestAgglomerativeClustering(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        model: fn.Node = agglomerative_clustering()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.n_clusters, 2)
        self.assertEqual(clustering.metric, Metric.default())
        self.assertIsNone(clustering.memory)
        self.assertIsNone(clustering.connectivity)
        self.assertEqual(clustering.compute_full_tree, "auto")
        self.assertEqual(clustering.linkage, Linkage.default())
        self.assertIsNone(clustering.distance_threshold)
        self.assertFalse(clustering.compute_distances)

    async def test_custom_parameters(self):
        n_clusters = 3
        metric = Metric.l1.value
        memory = "memory_cache"
        connectivity = np.array([[1, 0, 0], [0, 1, 1], [0, 1, 1]])
        compute_full_tree = True
        linkage = Linkage.average.value
        distance_threshold = 0.5
        compute_distances = True
        model: fn.Node = agglomerative_clustering()
        model.inputs["n_clusters"].value = n_clusters
        model.inputs["metric"].value = metric
        model.inputs["memory"].value = memory
        model.inputs["connectivity"].value = connectivity
        model.inputs["compute_full_tree"].value = compute_full_tree
        model.inputs["linkage"].value = linkage
        model.inputs["distance_threshold"].value = distance_threshold
        model.inputs["compute_distances"].value = compute_distances
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.n_clusters, n_clusters)
        self.assertEqual(clustering.metric, metric)
        self.assertEqual(clustering.memory, memory)
        self.assertIs(clustering.connectivity, connectivity)
        self.assertEqual(clustering.compute_full_tree, compute_full_tree)
        self.assertEqual(clustering.linkage, linkage)
        self.assertEqual(clustering.distance_threshold, distance_threshold)
        self.assertTrue(clustering.compute_distances)

    async def test_memory_caching(self):
        memory = Memory(location="cachedir", verbose=0)
        model: fn.Node = agglomerative_clustering()
        model.inputs["memory"].value = memory
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.memory.__class__, Memory)

    async def test_callable_metric(self):
        def custom_metric(x, y):
            return np.sum(np.abs(x - y))

        model: fn.Node = agglomerative_clustering()
        model.inputs["metric"].value = custom_metric
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.metric, custom_metric)


class TestBirchFunction(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        model: fn.Node = birch()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertEqual(clustering.threshold, 0.5)
        self.assertEqual(clustering.branching_factor, 50)
        self.assertEqual(clustering.n_clusters, 3)
        self.assertTrue(clustering.compute_labels)
        self.assertTrue(clustering.copy)

    async def test_custom_parameters(self):
        threshold = 0.2
        branching_factor = 30
        n_clusters = 5
        compute_labels = False
        copy = False
        model: fn.Node = birch()
        model.inputs["threshold"].value = threshold
        model.inputs["branching_factor"].value = branching_factor
        model.inputs["n_clusters"].value = n_clusters
        model.inputs["compute_labels"].value = compute_labels
        model.inputs["copy"].value = copy
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.threshold, threshold)
        self.assertEqual(clustering.branching_factor, branching_factor)
        self.assertEqual(clustering.n_clusters, n_clusters)
        self.assertFalse(clustering.compute_labels)
        self.assertFalse(clustering.copy)

    async def test_n_clusters_sklearn_model(self):
        model1: fn.Node = agglomerative_clustering()
        model1.inputs["n_clusters"].value = 2
        self.assertIsInstance(model1, fn.Node)
        model: fn.Node = birch()
        model.inputs["n_clusters"].connect(model1.outputs["out"])

        # await model1
        await model

        self.assertIsInstance(model, fn.Node)
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.n_clusters, model1.outputs["out"].value)


class TestDBSCAN(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        model: fn.Node = dbscan()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.eps, 0.5)
        self.assertEqual(clustering.min_samples, 5)
        self.assertEqual(clustering.metric, Metric.default())
        self.assertEqual(clustering.algorithm, Algorithm.default())
        self.assertEqual(clustering.leaf_size, 30)
        self.assertIsNone(clustering.p)
        self.assertIsNone(clustering.n_jobs)

    async def test_custom_parameters(self):
        eps = 1.0
        min_samples = 10
        metric = Metric.manhattan.value
        metric_params = {"p": 2}
        algorithm = Algorithm.kd_tree.value
        leaf_size = 50
        p = 2
        n_jobs = -1
        model: fn.Node = dbscan()
        model.inputs["eps"].value = eps
        model.inputs["min_samples"].value = min_samples
        model.inputs["metric"].value = metric
        model.inputs["metric_params"].value = metric_params
        model.inputs["algorithm"].value = algorithm
        model.inputs["leaf_size"].value = leaf_size
        model.inputs["p"].value = p
        model.inputs["n_jobs"].value = n_jobs

        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.eps, eps)
        self.assertEqual(clustering.min_samples, min_samples)
        self.assertEqual(clustering.metric, metric)
        self.assertEqual(clustering.algorithm, algorithm)
        self.assertEqual(clustering.leaf_size, leaf_size)
        self.assertEqual(clustering.p, p)
        self.assertEqual(clustering.n_jobs, n_jobs)


class TestFeatureAgglomeration(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        model: fn.Node = feature_agglomeration()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.n_clusters, 2)
        self.assertEqual(clustering.metric, Metric.default())
        self.assertIsNone(clustering.memory)
        self.assertIsNone(clustering.connectivity)
        self.assertEqual(clustering.compute_full_tree, "auto")
        self.assertEqual(clustering.linkage, Linkage.default())
        self.assertEqual(clustering.pooling_func, np.mean.__name__)
        self.assertIsNone(clustering.distance_threshold)
        self.assertFalse(clustering.compute_distances)

    async def test_custom_parameters(self):
        n_clusters = 3
        metric = Metric.l1.value
        memory = "memory_cache"
        connectivity = np.array([[1, 0, 0], [0, 1, 1], [0, 1, 1]])
        compute_full_tree = True
        linkage = Linkage.average.value
        pooling_func = np.median
        distance_threshold = 0.5
        compute_distances = True
        model: fn.Node = feature_agglomeration()
        model.inputs["n_clusters"].value = n_clusters
        model.inputs["metric"].value = metric
        model.inputs["memory"].value = memory
        model.inputs["connectivity"].value = connectivity
        model.inputs["compute_full_tree"].value = compute_full_tree
        model.inputs["linkage"].value = linkage
        model.inputs["pooling_func"].value = pooling_func
        model.inputs["distance_threshold"].value = distance_threshold
        model.inputs["compute_distances"].value = compute_distances
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.n_clusters, n_clusters)
        self.assertEqual(clustering.metric, metric)
        self.assertEqual(clustering.memory, memory)
        self.assertIs(clustering.connectivity, connectivity)
        self.assertEqual(clustering.compute_full_tree, compute_full_tree)
        self.assertEqual(clustering.linkage, linkage)
        self.assertEqual(clustering.distance_threshold, distance_threshold)
        self.assertTrue(clustering.compute_distances)
        self.assertEqual(clustering.pooling_func, pooling_func)


class TestKMeans(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        model: fn.Node = kmeans()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.n_clusters, 8)
        self.assertEqual(clustering.init, "k-means++")
        self.assertEqual(clustering.n_init, "auto")
        self.assertEqual(clustering.max_iter, 300)
        self.assertEqual(clustering.tol, 1e-4)
        self.assertEqual(clustering.verbose, 0)
        self.assertIsNone(clustering.random_state)
        self.assertTrue(clustering.copy_x)
        self.assertEqual(clustering.algorithm, KMeansAlgorithm.default())

    async def test_custom_parameters(self):
        def custom_init(X, n_clusters):
            # Custom initialization logic here
            return np.random.rand(n_clusters, X.shape[1])

        n_clusters = 5
        init = custom_init
        n_init = 3
        max_iter = 150
        tol = 1e-3
        verbose = 1
        random_state = 42
        copy_x = False
        algorithm = (KMeansAlgorithm.elkan.value,)
        model: fn.Node = kmeans()
        model.inputs["n_clusters"].value = n_clusters
        model.inputs["init"].value = init
        model.inputs["n_init"].value = n_init
        model.inputs["max_iter"].value = max_iter
        model.inputs["tol"].value = tol
        model.inputs["verbose"].value = verbose
        model.inputs["random_state"].value = random_state
        model.inputs["copy_x"].value = copy_x
        model.inputs["algorithm"].value = algorithm
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.n_clusters, n_clusters)
        self.assertEqual(clustering.init, init)
        self.assertEqual(clustering.n_init, n_init)
        self.assertIs(clustering.max_iter, max_iter)
        self.assertEqual(clustering.tol, tol)
        self.assertEqual(clustering.verbose, verbose)
        self.assertEqual(clustering.random_state, random_state)
        self.assertFalse(clustering.copy_x, copy_x)
        self.assertEqual(clustering.algorithm, algorithm)


class TestBisectingKMeans(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        model: fn.Node = bisecting_kmeans()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.n_clusters, 8)
        self.assertEqual(clustering.init, "k-means++")
        self.assertEqual(clustering.n_init, 1)
        self.assertIsNone(clustering.random_state)
        self.assertEqual(clustering.max_iter, 300)
        self.assertEqual(clustering.verbose, 0)
        self.assertEqual(clustering.tol, 1e-4)
        self.assertTrue(clustering.copy_x)
        self.assertEqual(
            clustering.algorithm, KMeansAlgorithm.default()
        )  # assuming KMeansAlgorithm.default() returns "lloyd"
        self.assertEqual(
            clustering.bisecting_strategy, BisectingStrategy.default()
        )  # assuming BisectingStrategy.default() returns "biggest_inertia"

    async def test_custom_parameters(self):
        def custom_init(X, n_clusters):
            # Custom initialization logic here
            return np.random.rand(n_clusters, X.shape[1])

        n_clusters = 5
        init = custom_init
        n_init = 3
        max_iter = 150
        tol = 1e-3
        verbose = 1
        random_state = 42
        copy_x = False
        algorithm = (KMeansAlgorithm.elkan.value,)
        model: fn.Node = bisecting_kmeans()
        model.inputs["n_clusters"].value = n_clusters
        model.inputs["init"].value = init
        model.inputs["n_init"].value = n_init
        model.inputs["max_iter"].value = max_iter
        model.inputs["tol"].value = tol
        model.inputs["verbose"].value = verbose
        model.inputs["random_state"].value = random_state
        model.inputs["copy_x"].value = copy_x
        model.inputs["algorithm"].value = algorithm
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        self.assertEqual(clustering.n_clusters, n_clusters)
        self.assertEqual(clustering.init, init)
        self.assertEqual(clustering.n_init, n_init)
        self.assertIs(clustering.max_iter, max_iter)
        self.assertEqual(clustering.tol, tol)
        self.assertEqual(clustering.verbose, verbose)
        self.assertEqual(clustering.random_state, random_state)
        self.assertFalse(clustering.copy_x, copy_x)
        self.assertEqual(clustering.algorithm, algorithm)


class TestMiniBatchKMeans(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        model: fn.Node = mini_batch_kmeans()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)
        # self.assertEqual(clustering.n_clusters, 8)
        # self.assertEqual(clustering.init, "k-means++")
        # self.assertEqual(clustering.n_init, 1)
        # self.assertIsNone(clustering.random_state)
        # self.assertEqual(clustering.max_iter, 300)
        # self.assertEqual(clustering.verbose, 0)
        # self.assertEqual(clustering.tol, 1e-4)
        # self.assertTrue(clustering.copy_x)
        # self.assertEqual(
        #     clustering.algorithm, KMeansAlgorithm.default()
        # )  # assuming KMeansAlgorithm.default() returns "lloyd"
        # self.assertEqual(
        #     clustering.bisecting_strategy, BisectingStrategy.default()
        # )  # assuming BisectingStrategy.default() returns "biggest_inertia"

    async def test_custom_parameters(self):
        def custom_init(X, n_clusters):
            # Custom initialization logic here
            return np.random.rand(n_clusters, X.shape[1])

        n_clusters = 5
        init = custom_init
        n_init = 3
        max_iter = 150
        model: fn.Node = mini_batch_kmeans()
        model.inputs["n_clusters"].value = n_clusters
        model.inputs["init"].value = init
        model.inputs["n_init"].value = n_init
        model.inputs["max_iter"].value = max_iter
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)

    async def test_predict(self):
        X = np.array([[1, 2], [1, 4], [1, 0], [4, 2], [4, 0], [4, 4]])

        n_clusters = 2
        batch_size = 3
        max_iter = 10
        n_init = 1
        model: fn.Node = mini_batch_kmeans()
        model.inputs["n_clusters"].value = n_clusters
        model.inputs["batch_size"].value = batch_size
        model.inputs["max_iter"].value = max_iter
        model.inputs["n_init"].value = n_init
        model.inputs["random_state"].value = 42
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        clustering.fit(X)
        self.assertIsInstance(clustering, ClusterMixin)
        np.testing.assert_array_equal(
            clustering.predict([[0, 0], [4, 4]]), np.array([0, 1])
        )


class TestMeanShift(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters_and_predict(self):
        X = np.array([[1, 1], [2, 1], [1, 0], [4, 7], [3, 5], [3, 6]])
        model: fn.Node = mean_shift()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        clustering.fit(X)
        self.assertIsInstance(clustering, ClusterMixin)
        np.testing.assert_array_equal(clustering.labels_, [4, 3, 5, 0, 2, 1])
        np.testing.assert_array_equal(
            clustering.predict([[0, 0], [5, 5]]), np.array([5, 2])
        )

    async def test_custom_parameters(self):
        X = np.array([[1, 1], [2, 1], [1, 0], [4, 7], [3, 5], [3, 6]])
        bandwidth = 2
        seeds = np.array([[1, 1], [2, 1]])
        bin_seeding = True
        model: fn.Node = mean_shift()
        model.inputs["bandwidth"].value = bandwidth
        model.inputs["bin_seeding"].value = bin_seeding
        model.inputs["seeds"].value = seeds
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        clustering.fit(X)
        self.assertIsInstance(clustering, ClusterMixin)
        np.testing.assert_array_equal(clustering.seeds, seeds)
        self.assertEqual(clustering.bin_seeding, bin_seeding)
        self.assertEqual(clustering.bandwidth, bandwidth)
        np.testing.assert_array_equal(clustering.labels_, [0, 0, 0, 0, 0, 0])


class TestOPTICS(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        X = np.array([[1, 2], [2, 5], [3, 6], [8, 7], [8, 8], [7, 3]])
        model: fn.Node = optics()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        clustering.fit(X)
        self.assertIsInstance(clustering, ClusterMixin)
        np.testing.assert_array_equal(clustering.labels_, [0, 0, 0, 0, 0, 0])

    async def test_custom_parameters(self):
        X = np.array([[1, 2], [2, 5], [3, 6], [8, 7], [8, 8], [7, 3]])
        min_samples = 2
        model: fn.Node = optics()
        model.inputs["min_samples"].value = min_samples
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        clustering.fit(X)
        self.assertIsInstance(clustering, ClusterMixin)
        np.testing.assert_array_equal(clustering.labels_, [0, 0, 0, 1, 1, 1])


class TestSpectralClustering(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        model: fn.Node = spectral_clustering()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        self.assertIsInstance(clustering, ClusterMixin)

    async def test_custom_parameters(
        self,
    ):  # TODO: n_clusters and n_componenting conflicts in node. solve by changing the default from None to 8
        X = np.array([[1, 1], [2, 1], [1, 0], [4, 7], [3, 5], [3, 6]])
        n_clusters = 2
        assign_labels = AssignLabels.discretize.value
        random_state = 0
        model: fn.Node = spectral_clustering()
        model.inputs["n_clusters"].value = n_clusters
        # model.inputs["n_components"].value = n_components

        model.inputs["assign_labels"].value = assign_labels
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]

        clustering = out.value()
        # print(model.func.ef_funcmeta)
        clustering.fit(X)
        self.assertIsInstance(clustering, ClusterMixin)


class TestSpectralBiclustering(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        X = np.array([[1, 1], [2, 1], [1, 0], [4, 7], [3, 5], [3, 6]])
        model: fn.Node = spectral_biclustering()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        clustering.fit(X)
        self.assertIsInstance(clustering, BaseEstimator)

    async def test_custom_parameters(self):
        X = np.array([[1, 1], [2, 1], [1, 0], [4, 7], [3, 5], [3, 6]])
        n_clusters = 2
        random_state = 0
        model: fn.Node = spectral_biclustering()
        model.inputs["n_clusters"].value = n_clusters
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        clustering.fit(X)
        self.assertIsInstance(clustering, BaseEstimator)
        self.assertEqual(clustering.n_clusters, n_clusters)
        self.assertEqual(clustering.random_state, random_state)
        np.testing.assert_array_equal(clustering.row_labels_, [1, 1, 1, 0, 0, 0])


class TestSpectralCoclustering(unittest.IsolatedAsyncioTestCase):
    async def test_default_parameters(self):
        X = np.array([[1, 1], [2, 1], [1, 0], [4, 7], [3, 5], [3, 6]])
        model: fn.Node = spectral_coclustering()
        self.assertIsInstance(model, fn.Node)

        await model
        out = model.outputs["out"]
        clustering = out.value()
        clustering.fit(X)
        self.assertIsInstance(clustering, BaseEstimator)

    async def test_custom_parameters(self):
        X = np.array([[1, 1], [2, 1], [1, 0], [4, 7], [3, 5], [3, 6]])
        n_clusters = 2
        random_state = 0
        model: fn.Node = spectral_coclustering()
        model.inputs["n_clusters"].value = n_clusters
        model.inputs["random_state"].value = random_state
        self.assertIsInstance(model, fn.Node)
        await model
        out = model.outputs["out"]
        clustering = out.value()
        clustering.fit(X)
        self.assertIsInstance(clustering, BaseEstimator)
        self.assertEqual(clustering.n_clusters, n_clusters)
        self.assertEqual(clustering.random_state, random_state)
        np.testing.assert_array_equal(clustering.row_labels_, [0, 1, 1, 0, 0, 0])
