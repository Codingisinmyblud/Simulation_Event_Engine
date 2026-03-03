from ..base_model import BaseModel
from ...des.resources.server import Server
from ...des.random.rng import RNG
from ...des.metrics.collector import MetricsCollector
from ...des.scheduling.scheduler import Scheduler
from .config import DEFAULT_CONFIG
from .events import handle_job_arrival, handle_job_complete, handle_node_failure, handle_node_repair
from .policies import random_routing, round_robin_routing

class DatacenterModel(BaseModel):
    def __init__(self, config=None):
        full_config = DEFAULT_CONFIG.copy()
        if config:
            full_config.update(config)
        super().__init__(full_config)
        self.nodes = []

    def initialize(self, simulator):
        # Tools
        rng = RNG(self.config.get('seed', 42))
        metrics = MetricsCollector(simulator)
        sched = Scheduler(simulator)

        # Setup state
        simulator.state.register_resource('rng', rng)
        simulator.state.register_entity('metrics', metrics)
        simulator.state.register_entity('model', self)
        
        # Determine policy
        policy_name = self.config['routing_policy']
        self.policy = round_robin_routing if policy_name == 'round_robin' else random_routing
        simulator.state.register_entity('routing_state', {})

        # Create nodes
        for i in range(self.config['num_nodes']):
            node = Server(f"node_{i}", capacity=1)
            self.nodes.append(node)
            simulator.state.register_resource(node.name, node)
            
            # Initial failure events for nodes
            dt_fail = rng.exponential(1.0 / self.config['node_failure_rate'])
            sched.schedule_in(dt_fail, 'NodeFailure', {'node': node})

        # Kick off first arrival
        dt_arr = rng.exponential(1.0 / self.config['arrival_rate'])
        sched.schedule_in(dt_arr, 'JobArrival')

    def register_events(self, simulator):
        simulator.register_handler('JobArrival', handle_job_arrival)
        simulator.register_handler('ServerFree', handle_job_complete) 
        simulator.register_handler('NodeFailure', handle_node_failure)
        simulator.register_handler('NodeRepair', handle_node_repair)
