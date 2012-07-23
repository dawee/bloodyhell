import sys
import os

BLOODYHELL_PATH = os.path.abspath(os.path.dirname(__file__))

if not BLOODYHELL_PATH in sys.path:
    sys.path.append(BLOODYHELL_PATH)
