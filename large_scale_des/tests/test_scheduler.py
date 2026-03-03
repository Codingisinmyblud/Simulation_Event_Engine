import pytest
from large_scale_des.des.simulator import Simulator
from large_scale_des.des.scheduling.scheduler import Scheduler

def test_schedule_in():
    sim = Simulator()
    sched = Scheduler(sim)
    
    # Sim is at time 0
    sched.schedule_in(10.0, "TestEvent")
    
    assert len(sim.queue) == 1
    ev = sim.queue.peek()
    assert ev.time == 10.0
    assert ev.type == "TestEvent"

def test_cancel_event():
    sim = Simulator()
    sched = Scheduler(sim)
    
    eid = sched.schedule_in(5.0, "ToCancel")
    sched.schedule_in(10.0, "ToKeep")
    
    assert len(sim.queue) == 2
    
    canceled = sched.cancel(eid)
    assert canceled is not None
    assert canceled.type == "ToCancel"
    assert len(sim.queue) == 1
    
    assert sim.queue.peek().type == "ToKeep"
