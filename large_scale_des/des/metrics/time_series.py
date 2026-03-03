class TimeSeries:
    """
    Time-weighted averages and distributions.
    """
    def __init__(self, name):
        self.name = name
        self.points = []
        self.last_time = 0.0
        self.last_value = 0.0
        self.area_under_curve = 0.0

    def add(self, time, value):
        dt = time - self.last_time
        if dt > 0:
            self.area_under_curve += self.last_value * dt
        
        self.points.append((time, value))
        self.last_time = time
        self.last_value = value

    def time_average(self, current_time=None):
        if current_time is None:
            current_time = self.last_time
            
        dt = current_time - self.last_time
        area = self.area_under_curve
        if dt > 0:
            area += self.last_value * dt
            
        if current_time == 0:
            return 0
        return area / current_time

    def get_values(self):
        return {
            'points': self.points,
            'time_average': self.time_average()
        }
