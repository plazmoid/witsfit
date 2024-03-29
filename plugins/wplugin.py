from abc import ABC, abstractmethod
from time import sleep
from utils import CmdException
import multiprocessing as mp
import os
import signal

__all__ = ['WPlugin', 'WPluginForking']

class WPlugin(ABC):
    running = False

    def run(self, *args, **kwargs):
        
        def __run_process(pipe, *args, **kwargs):
            with pipe:
                pipe.send(self.process(*args, **kwargs))

        if self.running:
            raise CmdException(f'Module "{self.__class__.__name__}" is already running')
        sigint_once = False
        retval = ''
        parent_pipe, child_pipe = mp.Pipe()
        proc = mp.Process(target=__run_process, args=(child_pipe,) + args, kwargs=kwargs)
        try:
            self.running = True
            proc.start()
            while True:
                try:
                    if parent_pipe.poll():
                        retval = parent_pipe.recv()
                        break
                    if proc.exitcode is not None:
                        break
                    sleep(0.1)
                except KeyboardInterrupt:
                    if sigint_once:
                        print('\nHard kill')
                        proc.kill()
                    else:
                        sigint_once = True
                    pass
        finally:
            proc.join()
            self.running = False
        return retval

    @abstractmethod
    def process(self, *args, **kwargs) -> object:
        pass


class WPluginForking(WPlugin):

    def run(self, *args, **kwargs):
        pid = os.fork()
        try:
            if pid == 0:
                self.running = True
                signal.signal(signal.SIGINT, signal.SIG_IGN)
                self.process(*args, **kwargs)
            elif pid == -1:
                return -1
            else: # UNIX SOCKETS
                os.wait()
        finally:
            if pid == 0:
                os._exit(0)
            self.running = False