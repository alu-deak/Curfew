#!/usr/bin/env python3
import time
import signal
import sys
from config import load_config
from time_check import is_in_restricted_hours, is_in_any_restricted_hours
from shutdown import shutdown

def signal_handler(signum, frame):
    """处理信号，优雅退出"""
    print(f"收到信号 {signum}，准备退出...")
    sys.exit(0)

def main(config):
    # 获取配置
    restricted_hours_list = config.get('restricted_hours', [])
    # 兼容旧版配置
    if isinstance(restricted_hours_list, dict):
        restricted_hours_list = [restricted_hours_list]
    check_interval = 1
    debug = config.get('debug', False)
    
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("Curfew 启动，开始检测禁用时段")
    print("检测间隔: 1 秒")
    print("禁用时段列表:")
    for i, period in enumerate(restricted_hours_list, 1):
        print(f"  {i}. {period['start_hour']}:{period['start_minute']:02d} - {period['end_hour']}:{period['end_minute']:02d}")
    
    while True:
        if is_in_any_restricted_hours(restricted_hours_list):
            print("检测到当前时间在禁用时段内")
            break
        else:
            print("当前时间不在禁用时段内，1秒后再次检测")
            time.sleep(1)
    
    # 循环结束后执行关机
    print("准备执行关机命令")
    # 根据 debug 配置决定是否在调试模式下运行
    shutdown(config['shutdown_command'], debug=debug)
    
    print("Curfew 退出")

if __name__ == "__main__":
    config = load_config()
    # 检查是否在调试模式
    if config.get('debug', False):
        # 直接运行，不使用守护进程
        main(config)
    else:
        from daemon import DaemonContext
        with DaemonContext():
            main(config)