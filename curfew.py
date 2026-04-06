#!/usr/bin/env python3
import time
from config import load_config
from time_check import is_in_restricted_hours
from shutdown import shutdown

def main():
    config = load_config()
    
    if config:
        restricted = config['restricted_hours']
        check_interval = config.get('check_interval', 5)  # 默认5分钟
        debug = config.get('debug', False)
        
        while True:
            if is_in_restricted_hours(
                restricted['start_hour'],
                restricted['start_minute'],
                restricted['end_hour'],
                restricted['end_minute']
            ):
                # 测试模式，避免实际关机
                if debug:
                    shutdown(config['shutdown_command'], test_mode=True)
                    print("测试模式，未实际关机")
                else:
                    shutdown(config['shutdown_command'])
                break
            else:
                print(f"当前时间不在禁用时段内，{check_interval}分钟后再次检测")
                time.sleep(check_interval * 60)  # 转换为秒
    else:
        print("未找到配置文件，请先运行 welcome.py 进行配置")

if __name__ == "__main__":
    main()
