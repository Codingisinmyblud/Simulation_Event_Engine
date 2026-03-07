import pytest
from large_scale_des.des.event_queue import EventQueue
from large_scale_des.des.event import Event

def test_event_queue_ordering():
    q = EventQueue()
    q.push(Event(time=10.0, priority=1, type="A"))
    q.push(Event(time=5.0, priority=1, type="B"))
    q.push(Event(time=10.0, priority=0, type="C"))
    
    # Should be B (t=5), C (t=10, p=0), A (t=10, p=1)
    e1 = q.pop()
    assert e1.type == "B"
    e2 = q.pop()
    assert e2.type == "C"
    e3 = q.pop()
    assert e3.type == "A"

def test_empty_queue():
    q = EventQueue()
    assert q.pop() is None
