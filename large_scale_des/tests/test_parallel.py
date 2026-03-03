import pytest
from large_scale_des.models.datacenter.model import DatacenterModel
from large_scale_des.experiments.runner import ParallelRunner

def test_parallel_runner():
    runner = ParallelRunner(num_workers=2)
    configs = [
        {'num_nodes': 5, 'arrival_rate': 100.0, 'seed': 1},
        {'num_nodes': 5, 'arrival_rate': 100.0, 'seed': 2}
    ]
    
    results = runner.run_batch(DatacenterModel, configs, until=50)
    
    assert len(results) == 2
    assert 'metrics' in results[0]
    assert 'metrics' in results[1]
