import itertools

def generate_grid(parameter_dict):
    """
    Generates a list of dictionaries covering all combinations 
    of the provided parameter lists.
    """
    keys = parameter_dict.keys()
    values = parameter_dict.values()
    
    # Ensures all values are lists
    normalized_values = [v if isinstance(v, list) else [v] for v in values]
    
    combinations = list(itertools.product(*normalized_values))
    
    configs = []
    for combo in combinations:
        conf = {}
        for k, v in zip(keys, combo):
            conf[k] = v
        configs.append(conf)
        
    return configs
