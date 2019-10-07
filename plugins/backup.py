from .wplugin import WPlugin
from zipfile import ZipFile
from os.path import realpath, dirname, join as pjoin
from datetime import datetime
import base64
import os
import time
import sys
import settings
import subprocess


class WBackup(WPlugin): 


    def process(self, *args, **kwargs):
        pacman_freeze = '/tmp/pacman'
        os.system(f"pacman -Qq > {pacman_freeze}")
        bp_dir = pjoin(dirname(realpath(sys.argv[0])), settings.BCK_PATH)
        zip_name = datetime.now().strftime("%Y-%m-%d_%H:%M") + '_plazmoid.zip'
        with ZipFile(pjoin(bp_dir, zip_name), 'w') as zipf:
            zipf.write(pacman_freeze)
        os.unlink(pacman_freeze)