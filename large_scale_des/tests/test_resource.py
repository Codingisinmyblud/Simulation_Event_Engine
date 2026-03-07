import pytest
from large_scale_des.des.resources.resource import Resource

def test_resource_acquire_release():
    r = Resource("test", capacity=2)
    assert r.is_available()
    assert r.acquire(1)
    assert r.acquire(1)
    assert not r.acquire(1) # Full
    
    assert r.release(1)
    assert r.acquire(1)

def test_resource_invalid_release():
    r = Resource("test", capacity=1)
    assert not r.release(1) # Empty
