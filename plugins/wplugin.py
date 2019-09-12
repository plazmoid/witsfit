from abc import ABC, abstractmethod
from time import sleep
import multiprocessing as mp

plugged = {}

class WPlugin(ABC):
    
    def run(self, *args, **kwargs):
        retval = ''
        parent_pipe, child_pipe = mp.Pipe()
        proc = mp.Process(target=self.__run_process, args=(child_pipe,) + args, kwargs=kwargs)
        proc.start() # ловить прерывания
        try:
            while True:
                try:
                    if parent_pipe.poll():
                        retval = parent_pipe.recv()
                        break
                    if proc.exitcode is not None:
                        break
                    sleep(0.1)
                except KeyboardInterrupt:
                    #proc.kill()
                    pass
        finally:
            proc.join()
        return retval

    def __run_process(self, pipe, *args, **kwargs):
        with pipe:
            pipe.send(self.process(*args, **kwargs))

    @abstractmethod
    def process(self, *args, **kwargs) -> object:
        pass