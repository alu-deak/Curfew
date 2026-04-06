#!/usr/bin/env python3
import os
import subprocess
from config import load_config

def shutdown(shutdown_command, test_mode=False):
    print(f"执行关机命令: {shutdown_command}")
    try:
        config_data = load_config()
        debug = config_data.get('debug', False)
    except FileNotFoundError:
        debug = False
    
    if not debug and not test_mode:
        if isinstance(shutdown_command, list):
            subprocess.run(shutdown_command, check=True)

        else:
            os.system(shutdown_command)
    else:
        print("测试模式: 未执行实际关机操作")
