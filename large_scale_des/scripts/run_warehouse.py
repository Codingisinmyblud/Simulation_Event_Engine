import json
from large_scale_des.models.warehouse.model import WarehouseModel
from large_scale_des.des.simulator import Simulator

def main():
    config = {
        'num_picking_stations': 3,
        'order_arrival_rate': 5.0,
        'mean_pick_time': 2.0,
        'routing_strategy': 'shortest_queue'
    }
    
    print("Initializing Warehouse Model...")
    model = WarehouseModel(config)
    sim = Simulator(config)
    
    model.initialize(sim)
    model.register_events(sim)
    
    print("Running simulation until time 500...")
    sim.run(until=500)
    
    metrics = sim.state.get_entity('metrics')
    results = metrics.get_all_metrics()
    
    print("\nSimulation Complete. Key Metrics:")
    for k, v in results.items():
        if isinstance(v, dict) and 'count' in v:
            print(f"- {k}: count={v['count']}, mean={v.get('mean', 0):.2f}, p99={v.get('p99', 0):.2f}")

if __name__ == "__main__":
    main()
