#!/usr/bin/env python3
from config import load_config, save_config
from consolemenu import ConsoleMenu

# 全局变量
config = None
restricted_hours_list = []
modified = False

def display_schedule():
    print("\n当前时间段列表:")
    if not restricted_hours_list:
        print("  暂无时间段")
        return
    
    for i, period in enumerate(restricted_hours_list, 1):
        print(f"  {i}. {period['start_hour']}:{period['start_minute']:02d} - {period['end_hour']}:{period['end_minute']:02d}")

def add_period():
    print("\n添加新时间段:")
    start_hour = int(input("开始小时 (0-23): "))
    start_minute = int(input("开始分钟 (0-59): "))
    end_hour = int(input("结束小时 (0-23): "))
    end_minute = int(input("结束分钟 (0-59): "))
    
    new_period = {
        'start_hour': start_hour,
        'start_minute': start_minute,
        'end_hour': end_hour,
        'end_minute': end_minute
    }
    
    restricted_hours_list.append(new_period)
    global modified
    modified = True
    print("时间段添加成功")

def edit_period():
    if not restricted_hours_list:
        print("暂无时间段可编辑")
        return
    
    display_schedule()
    index = int(input("请输入要编辑的时间段编号: ")) - 1
    if 0 <= index < len(restricted_hours_list):
        period = restricted_hours_list[index]
        print("\n编辑时间段:")
        print(f"当前时间: {period['start_hour']}:{period['start_minute']:02d} - {period['end_hour']}:{period['end_minute']:02d}")
        
        start_hour = int(input(f"开始小时 (0-23) [默认: {period['start_hour']}]: ") or period['start_hour'])
        start_minute = int(input(f"开始分钟 (0-59) [默认: {period['start_minute']}]: ") or period['start_minute'])
        end_hour = int(input(f"结束小时 (0-23) [默认: {period['end_hour']}]: ") or period['end_hour'])
        end_minute = int(input(f"结束分钟 (0-59) [默认: {period['end_minute']}]: ") or period['end_minute'])
        
        updated_period = {
            'start_hour': start_hour,
            'start_minute': start_minute,
            'end_hour': end_hour,
            'end_minute': end_minute
        }
        
        restricted_hours_list[index] = updated_period
        global modified
        modified = True
        print("时间段编辑成功")
    else:
        print("无效的时间段编号")

def delete_period():
    if not restricted_hours_list:
        print("暂无时间段可删除")
        return
    
    display_schedule()
    index = int(input("请输入要删除的时间段编号: ")) - 1
    if 0 <= index < len(restricted_hours_list):
        restricted_hours_list.pop(index)
        global modified
        modified = True
        print("时间段删除成功")
    else:
        print("无效的时间段编号")

def save():
    global modified
    if modified:
        config['restricted_hours'] = restricted_hours_list
        save_config(config)
        print("配置已保存")
        modified = False
    else:
        print("无修改需要保存")

def confirm_exit():
    global modified
    if modified:
        confirm = input("有未保存的修改，确定要放弃吗？(y/n): ")
        if confirm.lower() != 'y':
            return
    print("退出编辑器")
    exit()

def main():
    global config, restricted_hours_list
    try:
        config = load_config()
    except FileNotFoundError:
        print("配置文件不存在，请先运行 main.py 进行初始化")
        return
    
    # 获取并标准化时间段列表
    restricted_hours_list = config.get('restricted_hours', [])
    if isinstance(restricted_hours_list, dict):
        restricted_hours_list = [restricted_hours_list]
    
    # 创建菜单项字典
    menu_items = {
        "查看当前时间段列表": display_schedule,
        "添加新时间段": add_period,
        "编辑现有时间段": edit_period,
        "删除时间段": delete_period,
        "保存": save
    }
    
    # 创建主菜单
    menu = ConsoleMenu("时间段编辑器", menu_items)
    
    # 执行菜单
    menu.execute()
    
    # 退出菜单后检查是否有未保存的修改
    confirm_exit()

if __name__ == "__main__":
    main()