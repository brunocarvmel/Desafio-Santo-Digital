import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

app_dir = os.path.join(current_dir, "..") 

sys.path.insert(0, app_dir)
