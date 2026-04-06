#!/usr/bin/env python3
import time
import signal
import sys
from config import load_config
from time_check import is_in_restricted_hours
from shutdown import shutdown

def signal_handler(signum, frame):
    """处理信号，优雅退出"""
    print(f"收到信号 {signum}，准备退出...")
    sys.exit(0)

def main():
    # 加载配置
    config = load_config()
    
    # 获取配置
    restricted = config['restricted_hours']
    check_interval = config.get('check_interval', 5)  # 默认5分钟
    debug = config.get('debug', False)
    
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("Curfew 启动，开始检测禁用时段")
    print(f"禁用时段: {restricted['start_hour']}:{restricted['start_minute']:02d} - {restricted['end_hour']}:{restricted['end_minute']:02d}")
    print(f"检测间隔: {check_interval} 分钟")
    
    while True:
        if is_in_restricted_hours(
            restricted['start_hour'],
            restricted['start_minute'],
            restricted['end_hour'],
            restricted['end_minute']
        ):
            print("检测到当前时间在禁用时段内")
            break
        else:
            print(f"当前时间不在禁用时段内，{check_interval}分钟后再次检测")
            # 睡眠指定的检测间隔
            time.sleep(check_interval * 60)
    
    # 循环结束后执行关机
    print("准备执行关机命令")
    # 根据 debug 配置决定是否在调试模式下运行
    if debug:
        print("调试模式，执行关机命令（模拟）")
        shutdown(config['shutdown_command'], test_mode=True)
    else:
        print("执行关机命令")
        shutdown(config['shutdown_command'])
    
    print("Curfew 退出")

if __name__ == "__main__":
    config = load_config()
    from daemon import DaemonContext
    with DaemonContext():
        main()