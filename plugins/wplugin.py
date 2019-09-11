from abc import ABC, abstractmethod

plugged = {}

class WPlugin(ABC):
    
    def __new__(cls, *args, **kwargs):
        instance = super(WPlugin, cls).__new__(cls, *args, **kwargs)
        plugged[cls.__name__] = instance # создавать инстанс в новом процессе
        return instance # для каждого плагина прописать поведение в интерактивном и фоновом режиме
    
    @abstractmethod
    def process(self, *args, **kwargs):
        pass