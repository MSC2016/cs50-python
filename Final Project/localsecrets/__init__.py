import sys
import os

# Dynamically add the 'dependencies' folder to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
dependencies_path = os.path.join(project_root, 'dependencies')

if dependencies_path not in sys.path:
    sys.path.insert(0, dependencies_path)
