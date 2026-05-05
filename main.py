#!/usr/bin/env python3
from config import load_config, save_config
from autostart import setup_autostart
import os
import sys

def select_option(options, title, subtitle=""):
    """简单的选择菜单"""
    print(f"\n{title}")
    if subtitle:
        print(subtitle)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input("请选择: ")) - 1
            if 0 <= choice < len(options):
                return choice
            else:
                print("无效选项，请重新选择")
        except ValueError:
            print("无效输入，请输入数字")

def setup_config():
    mode_options = ["Windows 系统模式", "Linux 系统模式", "自定义模式"]
    mode_choice = select_option(mode_options, "请选择系统模式")
    
    # 操作类型选择
    action_options = ["关机", "睡眠"]
    action_choice = select_option(action_options, "请选择操作类型")
    
    # 根据选择设置配置
    if mode_choice == 0:
        # Windows 系统模式
        autostart_type = 'task scheduler'
        if action_choice == 0:
            shutdown_command = 'shutdown /s /t 0'
        else:
            shutdown_command = 'rundll32.exe powrprof.dll,SetSuspendState 0,1,0'
    elif mode_choice == 1:
        # Linux 系统模式
        autostart_type = 'systemd'
        if action_choice == 0:
            shutdown_command = ['shutdown', 'now']
        else:
            shutdown_command = ['systemctl', 'suspend']
    else:
        # 自定义模式
        autostart_options = ["Windows 计划任务", "systemd 服务 (Linux)", "稍后自行设置"]
        autostart_choice = select_option(autostart_options, "请选择自启动形式")
        
        autostart_map = {
            0: 'task scheduler',
            1: 'systemd',
            2: 'manual'
        }
        autostart_type = autostart_map.get(autostart_choice, 'manual')
        
        if action_choice == 0:
            print("\n请输入自定义关机命令:")
            print("例如: shutdown /s /t 0 或 sudo shutdown now")
        else:
            print("\n请输入自定义睡眠命令:")
            print("例如: rundll32.exe powrprof.dll,SetSuspendState 0,1,0 或 systemctl suspend")
        
        custom_command = input("请输入命令: ")
        # 检查是否需要以列表形式存储
        if ' ' in custom_command:
            shutdown_command = custom_command.split()
        else:
            shutdown_command = custom_command
    
    config = {
        'autostart_type': autostart_type,
        'shutdown_command': shutdown_command,
        'restricted_hours': {
            'workday': [],
            'weekend': [],
            'holiday': []
        },
        'continuous_usage_limits': {
            'workday': 0,
            'weekend': 0,
            'holiday': 0
        },
        'debug': False
    }
    
    save_config(config)
    print("配置已保存")
    
    print("\n提示：")
    print("- 您尚未配置禁用时段")
    print("- 请运行 schedule_editor.py 来添加和管理禁用时段")
    print("  命令：python3 schedule_editor.py")
    
    if autostart_type != 'manual':
        setup_autostart(autostart_type, os.path.abspath('curfew.py'))

def main():
    try:
        config = load_config()
        print("配置已存在，重新初始化配置...")
    except FileNotFoundError:
        print("首次启动，开始配置")
    
    setup_config()

if __name__ == "__main__":
    main()
