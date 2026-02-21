class SimulationState:
    """
    Holds global simulation state, registries, and configuration.
    """
    def __init__(self, config=None):
        self.sim_time = 0.0
        self.config = config or {}
        
        self.resources = {}
        self.entities = {}
        self.metrics = {}

    def register_resource(self, name, resource):
        self.resources[name] = resource

    def get_resource(self, name):
        return self.resources.get(name)

    def register_entity(self, name, entity):
        self.entities[name] = entity

    def get_entity(self, name):
        return self.entities.get(name)
