from settings import SOCKET_PATH
from threading import Thread
import os


if os.path.isfile(SOCKET_PATH):
    pass
else:
    from flask import Flask
    srv = Flask(__name__)
    from . import api
    Thread(target=srv.run).start()
    