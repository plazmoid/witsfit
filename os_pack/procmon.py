import psutil
import getpass
from pprint import pprint as pp

pp([p.info for p in psutil.process_iter(['pid', 'name', 'username', 'cmdline', 'memory_info']) 
        if p.info['username'] == getpass.getuser()])