import numpy as np
from numpy.typing import NDArray

from .gaussian_estimator import GaussianEstimator


class MaxLikelihoodEstimator(GaussianEstimator):

    def __init__(self) -> None:
        super().__init__()

    def estimate_parameters(self, features: NDArray) -> tuple[NDArray, NDArray]:
        mean = np.mean(features, axis=0)
        covariance = np.cov(features, rowvar=False)
        return mean, covariance
