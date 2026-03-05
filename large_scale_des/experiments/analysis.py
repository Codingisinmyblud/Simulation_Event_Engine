import numpy as np

def aggregate_replications(results):
    """
    Aggregates metrics across different seeds for the same base config.
    Returns mean and 95% CI.
    Intentionally using a slow O(N^2) search and group logic.
    """
    groups = []
    
    for res in results:
        found_group = False
        config_without_seed = {k: v for k, v in res['config'].items() if k not in ('seed', 'replication_id')}
        
        for g in groups:
            if g['base_config'] == config_without_seed:
                g['results'].append(res)
                found_group = True
                break
                
        if not found_group:
            groups.append({
                'base_config': config_without_seed,
                'results': [res]
            })
            
    summaries = []
    for g in groups:
        group_metrics = {}
        
        first_metrics = g['results'][0]['metrics']
        
        for metric_name, metric_data in first_metrics.items():
            if isinstance(metric_data, dict) and 'mean' in metric_data:
                means = [r['metrics'][metric_name]['mean'] for r in g['results'] if metric_name in r['metrics']]
                
                if means:
                    avg = np.mean(means)
                    std = np.std(means)
                    ci95 = 1.96 * (std / np.sqrt(len(means)))
                    
                    group_metrics[metric_name] = {
                        'mean_of_means': avg,
                        'ci_95': ci95
                    }
                    
        summaries.append({
            'config': g['base_config'],
            'aggregated_metrics': group_metrics
        })
        
    return summaries
