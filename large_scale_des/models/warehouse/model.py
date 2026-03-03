from ..base_model import BaseModel
from ...des.resources.server import Server
from ...des.random.rng import RNG
from ...des.metrics.collector import MetricsCollector
from ...des.scheduling.scheduler import Scheduler
from .config import DEFAULT_CONFIG
from .events import handle_order_arrival, handle_robot_arrival, handle_pick_complete
from .routing import shortest_queue_routing, random_routing

class WarehouseModel(BaseModel):
    def __init__(self, config=None):
        full_config = DEFAULT_CONFIG.copy()
        if config:
            full_config.update(config)
        super().__init__(full_config)
        self.stations = []

    def initialize(self, simulator):
        rng = RNG(self.config.get('seed', 42))
        metrics = MetricsCollector(simulator)
        sched = Scheduler(simulator)

        simulator.state.register_resource('rng', rng)
        simulator.state.register_entity('metrics', metrics)
        simulator.state.register_entity('model', self)
        
        strat_name = self.config['routing_strategy']
        self.routing_strategy = random_routing if strat_name == 'random' else shortest_queue_routing

        for i in range(self.config['num_picking_stations']):
            station = Server(f"station_{i}", capacity=1)
            self.stations.append(station)
            simulator.state.register_resource(station.name, station)
            
        # First order arrival
        dt_arr = rng.exponential(1.0 / self.config['order_arrival_rate'])
        sched.schedule_in(dt_arr, 'OrderArrival')

    def register_events(self, simulator):
        simulator.register_handler('OrderArrival', handle_order_arrival)
        simulator.register_handler('RobotArrivesAtStation', handle_robot_arrival)
        simulator.register_handler('ServerFree', handle_pick_complete) # Queue system core
