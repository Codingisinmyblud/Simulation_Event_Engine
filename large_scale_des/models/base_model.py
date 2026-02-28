class BaseModel:
    """
    Interface that all domain models must implement.
    """
    def __init__(self, config):
        self.config = config

    def initialize(self, simulator):
        """
        Set up resources, entities, state, and initial scheduled events.
        """
        raise NotImplementedError("Models must implement initialize()")

    def register_events(self, simulator):
        """
        Bind event types to their handlers.
        """
        raise NotImplementedError("Models must implement register_events()")
