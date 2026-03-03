import time
from .event_queue import EventQueue
from .state import SimulationState

class Simulator:
    def __init__(self, config=None):
        self.queue = EventQueue()
        self.state = SimulationState(config)
        self.handlers = {}
        self.running = False

    def register_handler(self, event_type, handler_fn):
        """
        Register a function to handle a specific event type.
        """
        self.handlers[event_type] = handler_fn

    def schedule(self, event):
        """
        Add an event to the queue.
        """
        self.queue.push(event)

    def run(self, until=float('inf')):
        """
        Main execution loop.
        Runs events until the simulation time exceeds 'until' or the queue is empty.
        """
        self.running = True
        
        while self.running and len(self.queue) > 0:
            next_event = self.queue.peek()
            
            if next_event.time > until:
                break
                
            next_event = self.queue.pop()
            
            self.state.sim_time = next_event.time
            
            handler = self.handlers.get(next_event.type)
            if handler:
                handler(self, next_event)
            else:
                print(f"Warning: No handler for event type {next_event.type}")
                
        self.running = False

    def stop(self):
        """Force stop the simulation loop."""
        self.running = False
