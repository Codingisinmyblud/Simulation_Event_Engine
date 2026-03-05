def with_replications(configs, num_replications, base_seed=42):
    """
    Expands a list of configs to include multiple random seeds.
    """
    replicated_configs = []
    
    for i in range(num_replications):
        for conf in configs:
            new_conf = conf.copy()
            new_conf['seed'] = base_seed + i
            new_conf['replication_id'] = i
            replicated_configs.append(new_conf)
            
    return replicated_configs
