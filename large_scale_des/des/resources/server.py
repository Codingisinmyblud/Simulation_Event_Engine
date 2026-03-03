from .resource import Resource
from .queue import FIFOQueue
from ..event import Event

class Server(Resource):
    """
    Capacity-based server handling a waiting line and service.
    """
    def __init__(self, name, capacity=1, queue=None):
        super().__init__(name, capacity)
        self.waiting_line = queue if queue else FIFOQueue()

    def request_service(self, entity, time, service_time, sim_callback):
        """
        Request service. If server has capacity, will process immediately
        and schedule completion event. Otherwise, entity waits.
        """
        # We need a callback to schedule the completion event on the simulator
        if self.acquire(1):
            completion_time = time + service_time
            sim_callback(Event(time=completion_time, type='ServerFree', payload={'entity': entity, 'server': self}))
            return True
        else:
            self.waiting_line.push((entity, service_time))
            return False

    def finish_service(self, time, sim_callback):
        """
        Release capacity and process next in line if any.
        """
        self.release(1)
        
        if len(self.waiting_line) > 0:
            # Promote next
            next_entity, next_svc_time = self.waiting_line.pop()
            self.acquire(1)
            completion_time = time + next_svc_time
            sim_callback(Event(time=completion_time, type='ServerFree', payload={'entity': next_entity, 'server': self}))
