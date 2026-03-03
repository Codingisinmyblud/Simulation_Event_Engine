import json
from large_scale_des.experiments.scenario import generate_grid
from large_scale_des.experiments.replication import with_replications
from large_scale_des.experiments.runner import ParallelRunner
from large_scale_des.experiments.analysis import aggregate_replications
from large_scale_des.models.datacenter.model import DatacenterModel

def main():
    print("Generating scenario grid...")
    params = {
        'num_nodes': [10, 20],
        'arrival_rate': [5.0, 10.0, 15.0],
        'routing_policy': ['random', 'round_robin']
    }
    
    base_configs = generate_grid(params)
    print(f"Generated {len(base_configs)} base configurations.")
    
    configs = with_replications(base_configs, num_replications=3)
    print(f"Total runs including seeds: {len(configs)}")
    
    print("\nRunning parallel experiments...")
    runner = ParallelRunner()
    results = runner.run_batch(DatacenterModel, configs, until=500)
    
    print("\nAggregating results across seeds...")
    summary = aggregate_replications(results)
    
    print("\nTop level results (latency vs config):")
    for s in summary:
        conf = s['config']
        metrics = s['aggregated_metrics']
        
        # Display wait time if available
        if 'job_wait_time' in metrics:
            wt = metrics['job_wait_time']['mean_of_means']
            print(f"Nodes:{conf['num_nodes']} Rate:{conf['arrival_rate']} Policy:{conf['routing_policy']:12} -> Avg Wait: {wt:.3f}")

if __name__ == "__main__":
    main()
