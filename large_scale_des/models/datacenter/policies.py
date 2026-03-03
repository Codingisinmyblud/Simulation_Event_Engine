def random_routing(nodes, rng):
    """Pick a random node from available ones."""
    available = []
    for node in nodes:
        if node.is_available():
            available.append(node)
            
    if not available:
        return None
        
    return rng.choice(available)

def round_robin_routing(nodes, state):
    """Simple round robin."""
    last_idx = state.get('last_rr_idx', -1)
    
    for i in range(len(nodes)):
        idx = (last_idx + 1 + i) % len(nodes)
        if nodes[idx].is_available():
            state['last_rr_idx'] = idx
            return nodes[idx]
            
    return None
