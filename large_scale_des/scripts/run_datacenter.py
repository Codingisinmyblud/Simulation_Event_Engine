import json
from large_scale_des.models.datacenter.model import DatacenterModel
from large_scale_des.des.simulator import Simulator

#to run this model, use ths command "PYTHONPATH=. python3 large_scale_des/scripts/run_datacenter.py"

def main():
    config = {
        'num_nodes': 10,
        'arrival_rate': 2.0,
        'mean_service_time': 3.0,
        'routing_policy': 'round_robin'
    }
    
    print("Initializing Datacenter Model...")
    model = DatacenterModel(config)
    sim = Simulator(config)
    
    model.initialize(sim)
    model.register_events(sim)
    
    print("Running simulation until time 1000...")
    sim.run(until=1000)
    
    metrics = sim.state.get_entity('metrics')
    results = metrics.get_all_metrics()
    
    print("\nSimulation Complete. Key Metrics:")
    for k, v in results.items():
        if isinstance(v, dict) and 'count' in v:
            print(f"- {k}: count={v['count']}, mean={v.get('mean', 0):.2f}, p99={v.get('p99', 0):.2f}")

if __name__ == "__main__":
    main()
