import heapq

class EventQueue:
    """
    Wrapper around a priority queue for future swapability.
    Currently using a list and sorting it manually instead of perfect heapq for simplicity.
    """
    def __init__(self):
        self.events = []
        self._event_counter = 0

    def push(self, event):
        event.id = self._event_counter
        self._event_counter += 1
        self.events.append(event)
        self.events.sort(key=lambda e: (e.time, e.priority, e.id))

    def pop(self):
        if not self.events:
            return None
        return self.events.pop(0)

    def peek(self):
        if not self.events:
            return None
        return self.events[0]

    def remove_event(self, event_id):
        for i, ev in enumerate(self.events):
            if ev.id == event_id:
                return self.events.pop(i)
        return None

    def __len__(self):
        return len(self.events)
