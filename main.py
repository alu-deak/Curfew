#!/usr/bin/env python3
from config import load_config, save_config
from autostart import setup_autostart
import os
import sys
import subprocess

def setup_config():
    # 系统模式选择
    print("请选择系统模式:")
    print("1. Windows 系统模式")
    print("2. Linux 系统模式")
    print("3. 自定义模式")
    mode_choice = input("请输入选项编号: ")
    
    # 操作类型选择
    print("\n请选择操作类型:")
    print("1. 关机")
    print("2. 睡眠")
    action_choice = input("请输入选项编号: ")
    # 验证输入有效性
    if action_choice not in ['1', '2']:
        print("无效选项，请重新运行程序")
        return
    
    # 根据选择设置配置
    if mode_choice == '1':
        # Windows 系统模式
        autostart_type = 'task scheduler'
        if action_choice == '1':
            shutdown_command = 'shutdown /s /t 0'
        else:
            shutdown_command = 'rundll32.exe powrprof.dll,SetSuspendState 0,1,0'
    elif mode_choice == '2':
        # Linux 系统模式
        autostart_type = 'systemd'
        if action_choice == '1':
            shutdown_command = ['shutdown', 'now']
        else:
            shutdown_command = ['systemctl', 'suspend']
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
        
        if action_choice == '1':
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
    
    print("\n请设置检测间隔 (分钟):")
    check_interval = int(input("检测间隔 (1-20): "))
    
    config = {
        'autostart_type': autostart_type,
        'shutdown_command': shutdown_command,
        'restricted_hours': [],
        'check_interval': check_interval,
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


def display_main_menu():
    print("\n===== Curfew 系统 =====")
    print("1. 重新初始化配置")
    print("2. 编辑禁用时段")
    print("3. 启动 Curfew 主程序")
    print("4. 退出")
    choice = input("请输入选项编号: ")
    return choice

def main():
    try:
        config = load_config()
    except FileNotFoundError:
        config = None
    
    if not config:
        print("首次启动，开始配置")
        setup_config()
    
    while config:
        choice = display_main_menu()
        
        if choice == '1':
            print("开始重新配置")
            setup_config()
        elif choice == '2':
            print("启动时段编辑器...")
            try:
                subprocess.run([sys.executable, 'schedule_editor.py'])
            except Exception as e:
                print(f"运行时段编辑器失败: {e}")
        elif choice == '3':
            print("启动 Curfew 主程序...")
            try:
                subprocess.run([sys.executable, 'curfew.py'])
            except Exception as e:
                print(f"运行 Curfew 主程序失败: {e}")
        elif choice == '4':
            print("退出程序")
            break
        else:
            print("无效的选项，请重新输入")

if __name__ == "__main__":
    main()
