# Global Optimization through High-Resolution Sampling

This package provides functions to run a global optimization algorithm, specifically designed to explore the properties of high-dimensional functions through High-Resolution sampling. It is based on the [following paper](https://arxiv.org/abs/2410.13737). The package includes tools for defining functions, setting optimization parameters, generating samples, and visualizing empirical probabilities.

## Installation

The package is available through pip, and may be installed via:

```bash
pip install GlobalOptimizationHRLA
```

## Setup

In order to use this package, you need to define:

- The target function and its gradient.
- An initial distribution for the search space.

## Main Usage

### 1. Defining the Target Function and Gradient

The provided example uses the Rastrigin function as the target for optimization.

```python
import numpy as np

d = 10
U = lambda x: d + np.linalg.norm(x) ** 2 - np.sum(np.cos(2 * np.pi * x))
dU = lambda x: 2 * x + 2 * np.pi * np.sin(2 * np.pi * x)
```

### 2. Sampling from an Initial Distribution

Define an initial distribution from which samples are generated:

```python
initial = lambda: np.random.multivariate_normal(np.zeros(d) + 3, 10 * np.eye(d))
```

### 3. Running the Algorithm

To execute the global optimization algorithm, use the DNLA.Algorithm class.

```python
import GlobalOptimizationHRLA as HRLA

algorithm = HRLA.Algorithm(d=d, M=100, N=10, K=14000, h=0.01, title=title, U=U, dU=dU, initial=initial)
samples_filename = algorithm.generate_samples(As=[1,2,3,4], sim_annealing=False)
```

#### **Parameters:**

- **d** (_int_): Dimension of the search space.
- **M** (_int_): Number of particles in the swarm.
- **N** (_int_): Number of generations for resampling.
- **K** (_int_): Total number of iterations to perform.
- **h** (_float_): Step size for gradient descent.
- **title** (_str_): Title for the optimization, useful for organizing saved data.
- **U** (_function_): The target function to optimize.
- **dU** (_function_): The gradient of the target function.
- **initial** (_function_): The initial distribution for generating particles.
- **As** (_list_): List of tolerances or annealing factors to adjust optimization.
- **sim_annealing** (_bool_): Determines whether to apply simulated annealing (default is False).

#### **Returns:**

- **samples_filename** (_str_): Path to the file where generated samples are saved.

### 4. Post-processing and Plotting Results

After running the optimization, use the `PostProcessor` object to analyze and plot the empirical probabilities from the generated samples.

```python
postprocessor = HRLA.PostProcessor(samples_filename)
```

#### **Parameters:**

- **samples_filename** (_str_): The filename containing the generated samples data.

---

The PostProcessor object provides multiple methods. One is the `plot_empirical_probabilities` method, which generates a plot of the empirical probabilities for different tolerances.

```python
postprocessor.plot_empirical_probabilities(dpi=10, layout="32", tols=[1,2,3,4,5,6], running=False)
```

#### **Parameters:**

- **dpi** (_int_): Resolution of the plot, in dots per inch.
- **layout** (_str_): Layout of the plot, specified as a string. Must be one of `["13", "23", "32", "22"]` (default is `"23"`).
- **tols** (_list_): List of tolerances for computing empirical probabilities (default is `[1,2,3,4,5,6]`).
- **running** (_bool_): Whether to display the plot with a running average or not (default is `False`).

---

Another method is `compute_tables`, which generates tables of empirical means and standard deviations.

```python
postprocessor.compute_tables(measured=[K], dpi=100, mode="mean", running="True"")
```

#### **Parameters:**

- **measured** (_list_): List with iteration counts to measure the empirical probabilities.
- **dpi** (_int_): Resolution of the plot, in dots per inch.
- **mode** (_str_): Mode for computing the tables, specified as a string. Must be one of `["mean", "std", "best"]` (default is `"mean"`).
- **running** (_bool_): Whether to display the results are computed with a running average or not (default is `True`).

## Examples

Examples may in found in the [/examples](/examples) directory of the repository.
