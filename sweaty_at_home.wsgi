import os
import sys

os.chdir(os.path.dirname(__file__))
sys.path.insert(0, ".")

from thermostat import app as application
