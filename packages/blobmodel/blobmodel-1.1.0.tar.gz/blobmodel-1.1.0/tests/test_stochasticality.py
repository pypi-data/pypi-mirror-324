import pytest
from blobmodel import DefaultBlobFactory, BlobShapeImpl, BlobFactory, DistributionEnum


def test_mean_of_distribution():
    bf = DefaultBlobFactory()
    distributions_mean_1 = [
        DistributionEnum.exp,
        DistributionEnum.gamma,
        DistributionEnum.uniform,
        DistributionEnum.rayleigh,
        DistributionEnum.deg,
    ]
    distributions_mean_0 = [DistributionEnum.normal, DistributionEnum.zeros]

    for dist in distributions_mean_1:
        tmp = bf._draw_random_variables(
            dist=dist,
            free_parameter=1,
            num_blobs=10000,
        )
        assert 0.95 <= tmp.mean() <= 1.05

    for dist in distributions_mean_0:
        tmp = bf._draw_random_variables(
            dist=dist,
            free_parameter=1,
            num_blobs=10000,
        )
        assert -0.05 <= tmp.mean() <= 0.05


def test_not_implemented_distribution():
    with pytest.raises(KeyError):
        bf = DefaultBlobFactory(A_dist="something_different")
        bf.sample_blobs(1, 1, 1, BlobShapeImpl(), 1)


def test_abstract_mehtods():
    BlobFactory.__abstractmethods__ = set()

    class MyBlobFactory(BlobFactory):
        pass

    my_obj = MyBlobFactory()

    with pytest.raises(NotImplementedError):
        my_obj.sample_blobs(1, 1, 1, BlobShapeImpl(), 1)

    with pytest.raises(NotImplementedError):
        my_obj.is_one_dimensional()
