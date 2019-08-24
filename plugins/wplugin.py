from abc import ABC, abstractmethod

plugged = {}

class WPlugin(ABC):
    
    def __new__(cls, *args, **kwargs):
        instance = super(WPlugin, cls).__new__(cls, *args, **kwargs)
        plugged[cls.__name__] = instance
        return instance 
    
    @abstractmethod
    def process(self, *args, **kwargs):
        pass