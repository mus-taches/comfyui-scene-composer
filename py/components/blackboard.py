from ..utils.config import load_config


class Singleton(type):
    """
    Ensure that only one instance of the class exists.
    """
    _instances = {}

    def __call__(cls, *arg, **kw):
        if cls not in cls._instances:
            instance = super().__call__(*arg, **kw)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Blackboard(metaclass=Singleton):
    """
    Store data so all nodes can modify and access it.
    """

    def __init__(self):
        self.variables = load_config("variables", with_filename=False)
        self.config = load_config("nodes")
