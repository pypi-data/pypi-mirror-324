import time
import os
import numpy as np
from tqdm import tqdm
import multiprocess as mp
import dill

class AlgorithmClass:
    def __init__(self, d, M, N, K, h, title, U, dU, initial):
        print(f"Initializing Algorithm for {title} with d={d}, M={M}, N={N}, K={K}, h={h}")
        self.d = d
        self.M = M
        self.N = N
        self.K = K
        self.h = h

        self.title = title
        self.U = U
        self.dU = dU
        self.initial = initial

    def __get_samples(self, a, sim_annealing, seed=None):
        # Set random seed if specified
        if seed: np.random.seed(seed)

        # Empty array to store iterates
        samples = np.zeros((self.N, self.K, self.d))

        # Sample N samples
        for n in range(self.N):
            # Initial sample
            x0 = self.initial()
            y0 = np.zeros(self.d)

            # Perform K iterations
            for k in range(self.K):
                # Determine value of a
                if sim_annealing:
                    start_a = 0.1
                    ak = (a - start_a) / self.K * k + start_a
                else:
                    ak = a

                # Perform iteration
                x0, y0 = self.__iterate(x0, y0, ak)
                samples[n, k] = x0

        return samples

    def generate_samples(self, As, sim_annealing):
        print(f"Generating samples for a in {As} with sim_annealing={sim_annealing}")

        # Function to generate samples
        generate_task = lambda task_nb: np.array([self.__get_samples(a, sim_annealing, seed=42+task_nb) for a in As])

        # Generate samples in parallel
        with mp.Pool() as pool:
            samples = list(tqdm(pool.imap(generate_task, range(self.M)), total=self.M, desc="Generating Samples"))

        # Format the data to save it
        samples_filename = f'temp_output/data/{self.title}_{time.time()}.pickle'
        samples_data = {
            "samples": samples,
            "title": self.title,
            "U": self.U,
            "dU": self.dU,
            "intial": self.initial,
            "d": self.d,
            "M": self.M,
            "N": self.N,
            "K": self.K,
            "h": self.h,
            "As": As,
            "sim_annealing": sim_annealing,
        }

        # Save all the data
        if not os.path.exists("temp_output"):
            os.makedirs("temp_output")
        if not os.path.exists("temp_output/data"):
            os.makedirs("temp_output/data")
        with open(samples_filename, 'wb') as handle:
            dill.dump(samples_data, handle)
            print(f"[SUCCESS] Samples dumped successfully into file {samples_filename}")

        return samples_filename

    def __iterate(self, x0, y0, a):
        raise NotImplementedError("The iterate method must be implemented in the child class")

class Algorithm(AlgorithmClass):
    def __init__(self, d, M, N, K, h, title, U, dU, initial):
        super().__init__(d, M, N, K, h, title, U, dU, initial)

    def __iterate(self, x0, y0, a):
        print("Iterate")
        # Compute parameters of algorithms
        delta   = self.h
        alpha   = 1
        beta    = 1
        gamma   = a / 10
        sigx2   = beta / a
        sigy2   = alpha / 10

        # delta   = self.h
        # alpha   = 1
        # beta    = 1
        # gamma   = 1
        # sigx2   = beta / a
        # sigy2   = alpha * gamma / a

        # Pre-compute values, to avoid repeated computations
        e       = np.exp(-alpha*delta)
        e2      = np.exp(-2*alpha*delta)
        dU0 = self.dU(x0)

        # Compute mean matrix
        mean_x = x0 - beta * delta * dU0 + (1 - e) / alpha * y0 - gamma / alpha * (delta - (1 - e) / alpha) * dU0
        mean_y = e * y0 - gamma / alpha * (1 - e) * dU0
        mean_matrix = np.block([mean_x, mean_y])

        # Compute covariance matrix
        cov_xx = (2 * sigx2 * delta + sigy2 / alpha ** 3 * (2 * alpha * delta + 1 - e2 - 4 * (1 - e))) * np.eye(self.d)
        cov_yy = sigy2 * (1 - e2) / alpha * np.eye(self.d)
        cov_xy = sigy2 * (1 - e) ** 2 / alpha ** 2 * np.eye(self.d)
        cov_matrix = np.block([[cov_xx, cov_xy], [cov_xy, cov_yy]])

        # Sample new point
        znew = np.random.multivariate_normal(mean_matrix.astype(float), cov_matrix.astype(float))

        return znew[:self.d], znew[self.d:]
