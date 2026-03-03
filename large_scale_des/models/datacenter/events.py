from ...des.scheduling.scheduler import Scheduler

def handle_job_arrival(simulator, event):
    """Spawns a new job and schedules the next arrival."""
    model = simulator.state.get_entity('model')
    rng = simulator.state.get_resource('rng')
    sched = Scheduler(simulator)
    
    # 1. Schedule next arrival
    dt = rng.exponential(1.0 / model.config['arrival_rate'])
    sched.schedule_in(dt, 'JobArrival')

    # 2. Process this arrival
    job_id = simulator.state.config.get('job_counter', 0)
    simulator.state.config['job_counter'] = job_id + 1
    
    # Route to node
    routing_state = simulator.state.entities.get('routing_state', {})
    node = model.policy(model.nodes, routing_state)
    
    if node:
        svc_time = rng.exponential(model.config['mean_service_time'])
        node.request_service(
            entity={'id': job_id},
            time=simulator.state.sim_time,
            service_time=svc_time,
            sim_callback=simulator.schedule
        )
        metrics = simulator.state.get_entity('metrics')
        metrics.record_summary('job_wait_time', 0.0)
    else:
        metrics = simulator.state.get_entity('metrics')
        metrics.record_summary('jobs_dropped', 1)

def handle_job_complete(simulator, event):
    """Job finishes on a node."""
    node = event.payload['server']
    node.finish_service(simulator.state.sim_time, simulator.schedule)
    
    metrics = simulator.state.get_entity('metrics')
    metrics.record_summary('jobs_completed', 1)

def handle_node_failure(simulator, event):
    """A node goes down."""
    node = event.payload['node']
    node.capacity = 0 

    model = simulator.state.get_entity('model')
    rng = simulator.state.get_resource('rng')
    sched = Scheduler(simulator)
    
    repair_time = rng.exponential(model.config['mean_repair_time'])
    sched.schedule_in(repair_time, 'NodeRepair', {'node': node})

def handle_node_repair(simulator, event):
    """A node comes back up."""
    node = event.payload['node']
    node.capacity = 1 

    model = simulator.state.get_entity('model')
    rng = simulator.state.get_resource('rng')
    sched = Scheduler(simulator)
    
    fail_time = rng.exponential(1.0 / model.config['node_failure_rate'])
    sched.schedule_in(fail_time, 'NodeFailure', {'node': node})
