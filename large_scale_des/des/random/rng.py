import numpy as np

class RNG:
    """
    Seeded RNG wrapper to ensure reproducibility per run.
    """
    def __init__(self, seed=None):
        self._rng = np.random.default_rng(seed)

    def exponential(self, scale):
        return self._rng.exponential(scale)

    def normal(self, loc, scale):
        return self._rng.normal(loc, scale)

    def uniform(self, low, high):
        return self._rng.uniform(low, high)

    def choice(self, a, p=None):
        return self._rng.choice(a, p=p)
