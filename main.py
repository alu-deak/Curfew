#!/usr/bin/env python3
from config import load_config, save_config
from autostart import setup_autostart
from consolemenu import ConsoleMenu
import os
import sys
import subprocess

def setup_config():
    # 系统模式选择
    # 由于consolemenu库版本问题，需要在函数内部导入SelectionMenu
    # 这里使用try-except来处理可能的导入错误
    try:
        from consolemenu.selection_menu import SelectionMenu
    except ImportError:
        # 如果导入失败，使用简单的命令行输入来替代
        def SelectionMenu(options, title, subtitle):
            class MockSelectionMenu:
                def __init__(self, options, title, subtitle):
                    self.options = options
                    self.title = title
                    self.subtitle = subtitle
                    self.selected_option = -1
                
                def show(self):
                    print(f"\n{self.title}")
                    if self.subtitle:
                        print(self.subtitle)
                    for i, option in enumerate(self.options, 1):
                        print(f"{i}. {option}")
                    while True:
                        try:
                            choice = int(input("请选择: ")) - 1
                            if 0 <= choice < len(self.options):
                                self.selected_option = choice
                                break
                            else:
                                print("无效选项，请重新选择")
                        except ValueError:
                            print("无效输入，请输入数字")
            return MockSelectionMenu(options, title, subtitle)
    mode_options = ["Windows 系统模式", "Linux 系统模式", "自定义模式"]
    mode_menu = SelectionMenu(mode_options, title="请选择系统模式", subtitle="")
    mode_menu.show()
    mode_choice = str(mode_menu.selected_option + 1)
    
    # 操作类型选择
    action_options = ["关机", "睡眠"]
    action_menu = SelectionMenu(action_options, title="请选择操作类型", subtitle="")
    action_menu.show()
    action_choice = str(action_menu.selected_option + 1)
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
        autostart_options = ["Windows 计划任务", "systemd 服务 (Linux)", "稍后自行设置"]
        autostart_menu = SelectionMenu(autostart_options, title="请选择自启动形式", subtitle="")
        autostart_menu.show()
        autostart_choice = str(autostart_menu.selected_option + 1)
        
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
    
    config = {
        'autostart_type': autostart_type,
        'shutdown_command': shutdown_command,
        'restricted_hours': {
            'workday': [],
            'weekend': [],
            'holiday': []
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


def reinitialize_config():
    print("开始重新配置")
    setup_config()

def edit_schedule():
    print("启动时段编辑器...")
    try:
        subprocess.run([sys.executable, 'schedule_editor.py'])
    except Exception as e:
        print(f"运行时段编辑器失败: {e}")

def start_curfew():
    print("启动 Curfew 主程序...")
    try:
        subprocess.run([sys.executable, 'curfew.py'])
    except Exception as e:
        print(f"运行 Curfew 主程序失败: {e}")

def main():
    try:
        config = load_config()
    except FileNotFoundError:
        config = None
    
    if not config:
        print("首次启动，开始配置")
        setup_config()
    
    # 创建菜单项字典
    menu_items = {
        "重新初始化配置": reinitialize_config,
        "编辑禁用时段": edit_schedule,
        "启动 Curfew 主程序": start_curfew
    }
    
    # 创建主菜单
    menu = ConsoleMenu("Curfew 系统", menu_items)
    
    # 执行菜单
    menu.execute()

if __name__ == "__main__":
    main()
