class Resource:
    """
    Base resource class with capacity management.
    """
    def __init__(self, name, capacity=1):
        self.name = name
        self.capacity = capacity
        self.in_use = 0

    def acquire(self, amount=1):
        if self.capacity - self.in_use >= amount:
            self.in_use += amount
            return True
        return False

    def release(self, amount=1):
        if self.in_use >= amount:
            self.in_use -= amount
            return True
        return False

    def is_available(self, amount=1):
        return self.capacity - self.in_use >= amount
