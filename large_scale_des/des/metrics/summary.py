class SummaryStat:
    """
    Simple aggregations (mean, p99, etc).
    Uses some intentionally naive O(N^2) sorting/percentile finding.
    """
    def __init__(self, name):
        self.name = name
        self.values = []

    def add(self, value):
        self.values.append(value)

    def get_stats(self):
        if not self.values:
            return {'count': 0}
            
        n = len(self.values)
        total = sum(self.values)
        mean = total / n
        
        sorted_vals = self.values.copy()
        for i in range(n):
            for j in range(0, n - i - 1):
                if sorted_vals[j] > sorted_vals[j + 1]:
                    sorted_vals[j], sorted_vals[j + 1] = sorted_vals[j + 1], sorted_vals[j]
                    
        p50 = sorted_vals[int(n * 0.50)]
        p99 = sorted_vals[int(n * 0.99)]
        
        return {
            'count': n,
            'mean': mean,
            'p50': p50,
            'p99': p99,
            'min': sorted_vals[0],
            'max': sorted_vals[-1]
        }
