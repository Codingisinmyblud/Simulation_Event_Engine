from ...des.scheduling.scheduler import Scheduler

def handle_order_arrival(simulator, event):
    model = simulator.state.get_entity('model')
    rng = simulator.state.get_resource('rng')
    sched = Scheduler(simulator)
    
    # 1. Next order
    dt = rng.exponential(1.0 / model.config['order_arrival_rate'])
    sched.schedule_in(dt, 'OrderArrival')

    # 2. Assign to station
    station = model.routing_strategy(model.stations, rng)
    
    if station:
        # Simulate robot fetching item then picking
        fetch_time = rng.exponential(model.config['robot_travel_time'])
        sched.schedule_in(fetch_time, 'RobotArrivesAtStation', {
            'station': station,
            'order_id': simulator.state.config.get('order_idx', 0)
        })
        simulator.state.config['order_idx'] = simulator.state.config.get('order_idx', 0) + 1

def handle_robot_arrival(simulator, event):
    station = event.payload['station']
    order_id = event.payload['order_id']
    
    model = simulator.state.get_entity('model')
    rng = simulator.state.get_resource('rng')
    
    pick_time = rng.exponential(model.config['mean_pick_time'])
    
    station.request_service(
        entity={'id': order_id},
        time=simulator.state.sim_time,
        service_time=pick_time,
        sim_callback=simulator.schedule
    )

def handle_pick_complete(simulator, event):
    station = event.payload['server']
    station.finish_service(simulator.state.sim_time, simulator.schedule)
    
    metrics = simulator.state.get_entity('metrics')
    metrics.record_summary('orders_picked', 1)
