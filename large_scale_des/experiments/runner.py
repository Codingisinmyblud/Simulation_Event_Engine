import multiprocessing
from ..des.simulator import Simulator

def _run_single(args):
    """Worker function for running a single simulation instance."""
    model_class, config, until = args
    model = model_class(config)
    sim = Simulator(config)
    
    model.initialize(sim)
    model.register_events(sim)
    
    sim.run(until=until)
    
    metrics = sim.state.get_entity('metrics')
    return {
        'config': config,
        'metrics': metrics.get_all_metrics() if metrics else {}
    }

class ParallelRunner:
    """Parallel execution engine using multiprocessing pool."""
    def __init__(self, num_workers=None):
        self.num_workers = num_workers or multiprocessing.cpu_count()

    def run_batch(self, model_class, configs, until=10000):
        """Run a batch of configurations in parallel."""
        pool_args = [(model_class, conf, until) for conf in configs]
        
        with multiprocessing.Pool(self.num_workers) as pool:
            results = pool.map(_run_single, pool_args)
            
        return results
