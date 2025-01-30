from .Algorithm import Algorithm
import numpy as np

class ULA_New(Algorithm):
    def __init__(self, d, M, N, K, h, title, U, dU, initial, L=1):
        print(f"ULA instantiating {title}")
        self.L = L
        super().__init__(d, M, N, K, h, title, U, dU, initial)

    def _iterate(self, x0, y0, a):
        # Compute parameters of algorithms
        h   = self.h

        gamma = 2
        xi = 2 * self.L

        # Pre-compute values, to avoid repeated computations
        e = np.exp(-gamma * xi * h)
        dU0 = self.dU(x0)

        # Compute mean matrix
        mean_x = x0 + (1 - e) / gamma * y0 - 1 / gamma * (h - (1 - e) / (gamma * xi)) * dU0
        mean_v = e * y0 - 1 / (gamma * xi) * (1 - e) * dU0
        mean_matrix = np.block([mean_x, mean_v])

        # Compute covariance matrix
        cov_xx = 1 / gamma * (2 * h - 3 / (gamma * xi) + 4 * e / (gamma * xi) - e ** 2 / (gamma * xi)) * np.eye(self.d)
        cov_vv = (1 - e ** 2) / xi * np.eye(self.d)
        cov_xv = (1 + e ** 2 - 2 * e) / (gamma * xi) * np.eye(self.d)
        cov_matrix = np.block([[cov_xx, cov_xv], [cov_xv, cov_vv]])

        # Sample new point
        znew = np.random.multivariate_normal(mean_matrix.astype(float), cov_matrix.astype(float))

        return znew[:self.d], znew[self.d:]