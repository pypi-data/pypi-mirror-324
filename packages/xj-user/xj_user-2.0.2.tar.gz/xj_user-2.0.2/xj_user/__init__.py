import os, sys
from pathlib import Path

# 引入内置库到环境变量
module_dir = Path(__file__).resolve().parent
sys.path.append(os.path.join(module_dir, 'libs'))
