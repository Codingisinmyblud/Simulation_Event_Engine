import time
from large_scale_des.models.datacenter.model import DatacenterModel
from large_scale_des.experiments.runner import ParallelRunner

def run_scaling_test():
    configs = [{'num_nodes': 50, 'arrival_rate': 20.0, 'seed': i} for i in range(16)]
    
    print("Testing parallel scaling...")
    
    # 1 Worker (Sequential)
    start_seq = time.time()
    runner_seq = ParallelRunner(num_workers=1)
    runner_seq.run_batch(DatacenterModel, configs, until=5000)
    end_seq = time.time()
    print(f"1 Worker: {end_seq - start_seq:.2f}s")
    
    # Max Workers (Parallel)
    start_par = time.time()
    runner_par = ParallelRunner()
    runner_par.run_batch(DatacenterModel, configs, until=5000)
    end_par = time.time()
    print(f"Max Workers: {end_par - start_par:.2f}s")
    
    speedup = (end_seq - start_seq) / (end_par - start_par)
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    run_scaling_test()
