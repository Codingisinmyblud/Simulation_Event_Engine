from ..event import Event

class Scheduler:
    """
    Encapsulates event scheduling logic.
    """
    def __init__(self, simulator):
        self.simulator = simulator

    def schedule(self, time, event_type, payload=None, priority=0):
        """Schedule an event at an absolute time."""
        if payload is None:
            payload = {}
        e = Event(time=time, type=event_type, payload=payload, priority=priority)
        self.simulator.schedule(e)
        return e.id

    def schedule_in(self, delta, event_type, payload=None, priority=0):
        """Schedule an event relative to current simulation time."""
        current_time = self.simulator.state.sim_time
        return self.schedule(current_time + delta, event_type, payload, priority)

    def cancel(self, event_id):
        """Cancel a previously scheduled event."""
        # This requires the queue to support removal
        return self.simulator.queue.remove_event(event_id)
