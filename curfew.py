#!/usr/bin/env python3
import time
import signal
import sys
from config import load_config
from time_check import is_in_restricted_hours_for_today
from shutdown import shutdown
from date_type import get_date_type

def signal_handler(signum, frame):
    """处理信号，优雅退出"""
    print(f"收到信号 {signum}，准备退出...")
    sys.exit(0)

def main(config):
    restricted_hours_dict = config.get('restricted_hours', {})
    continuous_usage_limits = config.get('continuous_usage_limits', {})
    check_interval = 1
    debug = config.get('debug', False)
    consecutive_seconds = 0

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Curfew 启动，开始检测禁用时段")
    print("检测间隔: 1 秒")

    date_type_names = {
        'workday': '工作日',
        'weekend': '周末',
        'holiday': '节假日'
    }

    print("连续使用时间限制:")
    for date_type in ['workday', 'weekend', 'holiday']:
        limit = continuous_usage_limits.get(date_type, 0)
        print(f"  {date_type_names[date_type]}: {limit} 分钟")
    
    for date_type in ['workday', 'weekend', 'holiday']:
        hours_list = restricted_hours_dict.get(date_type, [])
        print(f"{date_type_names[date_type]}禁用时段:")
        if hours_list:
            for i, period in enumerate(hours_list, 1):
                print(f"  {i}. {period['start_hour']}:{period['start_minute']:02d} - {period['end_hour']}:{period['end_minute']:02d}")
        else:
            print("  无")
    
    current_date_type = get_date_type()
    print(f"\n当前日期类型: {date_type_names[current_date_type]}")
    
    while True:
        if is_in_restricted_hours_for_today(restricted_hours_dict):
            print("检测到当前时间在禁用时段内")
            consecutive_seconds = 0
            break
        else:
            current_date_type = get_date_type()
            current_limit = continuous_usage_limits.get(current_date_type, 0)
            print(f"当前时间不在禁用时段内（{date_type_names[current_date_type]}），1秒后再次检测")
            time.sleep(1)
            consecutive_seconds += 1

            if current_limit > 0 and consecutive_seconds >= current_limit * 60:
                print(f"连续使用时间超过限制（{current_limit}分钟）")
                consecutive_seconds = 0
                break
    
    print("准备执行关机命令")
    shutdown(config['shutdown_command'], debug=debug)
    
    print("Curfew 退出")

if __name__ == "__main__":
    config = load_config()
    if config.get('debug', False):
        main(config)
    else:
        from daemon import DaemonContext
        with DaemonContext():
            main(config)