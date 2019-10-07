from flask import Flask
from witsfit import Witsfit, ALL_MODULES
from . import srv

wtf: Witsfit = Witsfit.instance ### Single instance

@srv.route("/info/")
def info():
    #return '\n'.join(wtf.enabled_modules)
    return '<br>'.join(f"{mod}: {cls_.__class__.__name__}" for mod, cls_ in ALL_MODULES.items() if cls_.running)
