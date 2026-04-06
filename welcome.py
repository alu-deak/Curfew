#!/usr/bin/env python3
from config import load_config, save_config
from autostart import setup_autostart
import os
import sys

def main():
    config = load_config()
    
    if not config:
        print("首次启动，开始配置")
        
        print("请选择系统模式:")
        print("1. Windows 系统模式")
        print("2. Linux 系统模式")
        print("3. 自定义模式")
        mode_choice = input("请输入选项编号: ")
        
        if mode_choice == '1':
            # Windows 系统模式
            autostart_type = 'task scheduler'
            shutdown_command = 'shutdown /s /t 0'
        elif mode_choice == '2':
            # Linux 系统模式
            autostart_type = 'systemd'
            shutdown_command = ['shutdown', 'now']
        else:
            # 自定义模式
            print("\n请选择自启动形式:")
            print("1. Windows 计划任务")
            print("2. systemd 服务 (Linux)")
            print("3. 稍后自行设置")
            autostart_choice = input("请输入选项编号: ")
            
            autostart_map = {
                '1': 'task scheduler',
                '2': 'systemd',
                '3': 'manual'
            }
            autostart_type = autostart_map.get(autostart_choice, 'manual')
            
            print("\n请输入自定义关机命令:")
            print("例如: shutdown /s /t 0 或 sudo shutdown now")
            custom_shutdown = input("请输入关机命令: ")
            # 检查是否需要以列表形式存储
            if ' ' in custom_shutdown:
                shutdown_command = custom_shutdown.split()
            else:
                shutdown_command = custom_shutdown
        
        print("\n请设置禁用时段 (24小时制):")
        start_hour = int(input("开始小时 (0-23): "))
        start_minute = int(input("开始分钟 (0-59): "))
        end_hour = int(input("结束小时 (0-23): "))
        end_minute = int(input("结束分钟 (0-59): "))
        
        print("\n请设置检测间隔 (分钟):")
        check_interval = int(input("检测间隔 (1-20): "))
        
        config = {
            'autostart_type': autostart_type,
            'shutdown_command': shutdown_command,
            'restricted_hours': {
                'start_hour': start_hour,
                'start_minute': start_minute,
                'end_hour': end_hour,
                'end_minute': end_minute
            },
            'check_interval': check_interval,
            'debug': False
        }
        
        save_config(config)
        print("配置已保存")
        
        if autostart_type != 'manual':
            setup_autostart(autostart_type, os.path.abspath('curfew.py'))
    else:
        print("配置文件已存在，如需重新配置请删除 config.json 文件后再次运行")

if __name__ == "__main__":
    main()
