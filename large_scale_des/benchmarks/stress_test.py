import time
from large_scale_des.models.datacenter.model import DatacenterModel
from large_scale_des.des.simulator import Simulator

def run_stress_test():
    print("Starting stress test: 1M events target...")
    
    config = {
        'num_nodes': 1000,
        'arrival_rate': 500.0,
        'mean_service_time': 2.0
    }
    
    model = DatacenterModel(config)
    sim = Simulator(config)
    model.initialize(sim)
    model.register_events(sim)
    
    start = time.time()
    sim.run(until=2000)
    end = time.time()
    
    events_processed = getattr(sim.queue, '_event_counter', 0)
    duration = end - start
    
    print(f"Processed {events_processed} events in {duration:.2f} seconds.")
    print(f"Throughput: {events_processed/duration:.2f} events/sec")

if __name__ == "__main__":
    run_stress_test()
