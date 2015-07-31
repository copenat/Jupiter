__author__ = 'Nathan'

import configparser
import os
import os.path
import logging
from src.JupiterUI.lib.JupiterUI import JupiterUIApp

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y%m%d %H:%M:%S')

configfile = 'JupiterUI.properties'
config = configparser.ConfigParser()
config.read(configfile)

app = JupiterUIApp(config)
app.mainloop()
