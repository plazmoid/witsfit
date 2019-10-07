from .wplugin import *
from importlib import import_module

ALL_MODULES = {
    'decoders': 'WDecoder',
    'proxies': 'WProxies',
    'backup': 'WBackup',
    'procmon': 'WProcessMonitor'
}

for k, v in ALL_MODULES.items():
    module = import_module(f'plugins.{k}')
    ALL_MODULES[k] = getattr(module, v)()
