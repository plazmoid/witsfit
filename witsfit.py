#!/usr/bin/env python3
from cmd import Cmd
from importlib import import_module
from utils import CmdException
import argparse
import settings
import sys


ALL_MODULES = import_module(settings.MODULES_PATH).ALL_MODULES

class Witsfit(Cmd):
    intro = settings.INTRO
    prompt = 'wtf> '
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self, *args, **kwargs):
        self.commands = ['start', 'stop', 'enable', 'disable']
        super().__init__(*args, **kwargs)

    def run_module(self, module, args):
        module = ALL_MODULES[module]
        #if module in self.enabled_modules:
        #    raise CmdException(f'Module "{module}" is already running')
        #self.enabled_modules.append(module)
        #print(Witsfit.enabled_modules)
        retval = module.run(args)
        #self.enabled_modules.remove(module)
        print(retval)

    def do_EOF(self, arg):
        sys.exit(0)

    def do_svc(self, arg):
        'Managing services'
        try:
            op, *module = arg.split()
            args = ''
            if len(module) > 1:
                args = ' '.join(module[1:])
            module = module[0]
        except (ValueError, IndexError):
            raise CmdException(f'Module was expected')

        if module not in ALL_MODULES:
            raise CmdException(f'Unknown module "{module}"')
        if op == 'on':
            self.run_module(module, args)
        elif op == 'off':
            if module not in self.enabled_modules:
                raise CmdException(f'Module "{module}" is already stopped')
        elif op == 'on_aex':
            raise CmdException('Not implemented')
        elif op == 'off_aex':
            raise CmdException('Not implemented')
        else:
            raise CmdException(f'"{op}" is not a command')


    def complete_svc(self, text, line, begidx, endidx):
        #print(f'*** "{text}", "{line}", {begidx}, {endidx}"')
        result = []
        for cmd in self.commands:
            if cmd.startswith(text):
                result.append(cmd)
            if cmd in line:
                if cmd == text:
                    return [text + ' ']
                else:
                    if text == '':
                        return list(ALL_MODULES.keys())
                    else:
                        return [mod for mod in ALL_MODULES if mod.startswith(text)]
        if begidx == endidx:
            return self.commands
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
                    print('KeyboardInterrupt')
            self.postloop()
        finally:
            if self.use_rawinput and self.completekey:
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass

    def emptyline(self):
        pass

    @classmethod
    def make_do(cls):
        def gen_do(fname):
            def do_smth(self, args):
                self.run_module(fname.replace('do_', ''), args)

            do_smth.__name__ = fname
            return do_smth

        for module in ALL_MODULES:
            do_fun = gen_do(f'do_{module}')
            setattr(cls, do_fun.__name__, do_fun)

Witsfit.make_do()

if __name__ == '__main__':
    import processes
    Witsfit().cmdloop()
    pass

# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('cmd', nargs='*', help='Command to execute') #non-interactive
#     parser.add_argument('-c', '--connect', action='store', default='localhost', #interactive
#                         dest='host', help=f'server or server:port to connect')
#     parser.add_argument('-d', '--debug', action='store_true',
#                         dest='debug', help='Debug mode')
#     parser.add_argument('-p', action='store_const', dest='port', const=settings.DEFAULT_PORT,
#                         help=f'Start server on port (default is {settings.DEFAULT_PORT})')
#     args = parser.parse_args()
    
    
#     if args.port:
#         #TODO: проверять на запущенность
#         server = importlib.import_module('server')
#         server.init(args.port)
#     else:
#         witsfit = Witsfit(host=args.host)
#         if args.cmd:
#             witsfit.parse_cmd(args.cmd)    
#         else:
#             witsfit.cmdloop()



