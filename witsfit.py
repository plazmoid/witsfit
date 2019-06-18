#!venv/bin/python3
from cmd import Cmd
import sys
import importlib

__author__ = 'p1azm0id'
__version__ = '0.0.3'

ALL_MODULES = ['net.proxies', 'memlimiter'] #TODO: сканировать директории
ENABLED_MODULES = [] #TODO: thread pool

INTRO = f"""
WITSFIT ({__version__}) - WTF IS IT (obviously i can't come up with a simple name lulz)
Big helper for the p1azm0id's dumb system

***************************************

Enabled modules: {', '.join(ENABLED_MODULES)}
"""
        
def do_nope(self):
    'Do literally nothing'
    print(f'did nothing {self}')

class CmdException(Exception): pass

class CmdError(Exception): pass

class Witsfit(Cmd):
    intro = INTRO
    prompt = 'wtf>'
    
    def __init__(self, *args, **kwargs):
        self.svc_commands = ['on', 'off', 'enable_aexec', 'disable_aexec']
        self.do_nop = do_nope
        super().__init__(*args, **kwargs)
    
    def do_EOF(self, arg):
        sys.exit(0)

    def do_svc(self, arg):
        'Managing services'
        try:
            op, module = arg.split()
        except ValueError:
            raise CmdException(f'Module was expected')
        
        if module not in ALL_MODULES:
            raise CmdException(f'Unknown module "{module}"')
        if op == 'on':
            if module in ENABLED_MODULES:
                raise CmdException(f'Module "{module}" is already running')
            module = importlib.import_module(module)
            module.start()
        elif op == 'off':
            if module not in ENABLED_MODULES:
                raise CmdException(f'Module "{module}" is already stopped')
        elif op == 'enable_aexec':
            raise CmdException('Not implemented')
        elif op == 'disable_aexec':
            raise CmdException('Not implemented')
        else:
            raise CmdException(f'"{op}" is not a command')
            
        
    def complete_svc(self, text, line, begidx, endidx):
        #print(f'*** "{text}", "{line}", {begidx}, {endidx}"')
        result = []
        for cmd in self.svc_commands:
            if cmd.startswith(text):
                result.append(cmd)
            if cmd in line:
                if cmd == text:
                    return [text + ' '] 
                else:
                    if text == '':
                        return ALL_MODULES
                    else:
                        return [mod for mod in ALL_MODULES if mod.startswith(text)]
        if begidx == endidx:
            return self.svc_commands
        return result
        
    def cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        """

        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                import readline
                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                readline.parse_and_bind(self.completekey+": complete")
            except ImportError:
                pass
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro)+"\n")
            stop = None
            while not stop:
                try:
                    if self.cmdqueue:
                        line = self.cmdqueue.pop(0)
                    else:
                        if self.use_rawinput:
                            try:
                                line = input(self.prompt)
                            except EOFError:
                                line = 'EOF'
                        else:
                            self.stdout.write(self.prompt)
                            self.stdout.flush()
                            line = self.stdin.readline()
                            if not len(line):
                                line = 'EOF'
                            else:
                                line = line.rstrip('\r\n')
                    line = self.precmd(line)
                    stop = self.onecmd(line)
                    stop = self.postcmd(stop, line)
                except CmdException as e:
                    print('ERR:' + str(e))
                except KeyboardInterrupt:
                    sys.exit(0)
            self.postloop()
        finally:
            if self.use_rawinput and self.completekey:
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass


if __name__ == '__main__':
    instance = Witsfit().cmdloop()
    