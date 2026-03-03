from .time_series import TimeSeries
from .summary import SummaryStat

class MetricsCollector:
    """
    Tracks time-based metrics and scalar values.
    """
    def __init__(self, simulator):
        self.simulator = simulator
        self.time_series = {}
        self.summaries = {}

    def get_time(self):
        return self.simulator.state.sim_time

    def record_timeseries(self, name, value):
        if name not in self.time_series:
            self.time_series[name] = TimeSeries(name)
        self.time_series[name].add(self.get_time(), value)

    def record_summary(self, name, value):
        if name not in self.summaries:
            self.summaries[name] = SummaryStat(name)
        self.summaries[name].add(value)

    def get_all_metrics(self):
        results = {}
        for k, v in self.time_series.items():
            results[k] = v.get_values()
        for k, v in self.summaries.items():
            results[k] = v.get_stats()
        return results
