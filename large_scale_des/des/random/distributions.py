class Distribution:
    """Base class for distributions."""
    def __init__(self, rng):
        self.rng = rng
        
    def sample(self):
        raise NotImplementedError

class Exponential(Distribution):
    def __init__(self, rng, rate):
        super().__init__(rng)
        self.scale = 1.0 / rate if rate > 0 else 0

    def sample(self):
        return self.rng.exponential(self.scale)

class Normal(Distribution):
    def __init__(self, rng, mu, sigma):
        super().__init__(rng)
        self.mu = mu
        self.sigma = sigma

    def sample(self):
        return self.rng.normal(self.mu, self.sigma)
