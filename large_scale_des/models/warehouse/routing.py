def shortest_queue_routing(stations, rng):
    """Find the picking station with the shortest waiting line."""
    best_station = None
    min_queue = float('inf')
    
    # O(n) scan
    for station in stations:
        q_len = len(station.waiting_line)
        if q_len < min_queue:
            min_queue = q_len
            best_station = station
            
    return best_station

def random_routing(stations, rng):
    """Pick a random station."""
    return rng.choice(stations)
