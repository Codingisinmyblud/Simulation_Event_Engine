class Queue:
    """
    Base definition of a queue discipline for waiting items.
    """
    def __init__(self):
        self.items = []

    def push(self, item):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def __len__(self):
        return len(self.items)

class FIFOQueue(Queue):
    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop(0)
        return None

class PriorityQueue(Queue):
    def push(self, item):
        self.items.append(item)
        # Prioritizaion uses sort on every push O(n log n) [!!!WILL CHANGE LATER!!!]
        # Assuming item is a tuple (priority, value) or has a priority attr
        self.items.sort(key=lambda x: getattr(x, 'priority', x[0] if isinstance(x, tuple) else 0))

    def pop(self):
        if self.items:
            return self.items.pop(0)
        return None

class LIFOQueue(Queue):
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        if self.items:
            return self.items.pop()
        return None
