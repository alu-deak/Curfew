#!/usr/bin/env python3
from config import load_config, save_config
from consolemenu import ConsoleMenu

config = None
restricted_hours_dict = {}
current_date_type = 'workday'
modified = False

date_type_names = {
    'workday': '工作日',
    'weekend': '周末',
    'holiday': '节假日'
}

def select_date_type():
    global current_date_type, modified
    print("\n选择日期类型:")
    print("1. 工作日")
    print("2. 周末")
    print("3. 节假日")
    
    while True:
        try:
            choice = int(input("请选择日期类型 (1-3): "))
            if choice == 1:
                current_date_type = 'workday'
                break
            elif choice == 2:
                current_date_type = 'weekend'
                break
            elif choice == 3:
                current_date_type = 'holiday'
                break
            else:
                print("无效选项，请输入 1-3")
        except ValueError:
            print("无效输入，请输入数字")
    
    print(f"当前编辑的是: {date_type_names[current_date_type]}")

def get_current_list():
    return restricted_hours_dict.get(current_date_type, [])

def set_current_list(new_list):
    global modified
    restricted_hours_dict[current_date_type] = new_list
    modified = True

def display_schedule():
    print(f"\n{date_type_names[current_date_type]}时间段列表:")
    current_list = get_current_list()
    if not current_list:
        print("  暂无时间段")
        return
    
    for i, period in enumerate(current_list, 1):
        print(f"  {i}. {period['start_hour']}:{period['start_minute']:02d} - {period['end_hour']}:{period['end_minute']:02d}")

def display_all_schedules():
    print("\n所有日期类型的时间段列表:")
    for date_type in ['workday', 'weekend', 'holiday']:
        hours_list = restricted_hours_dict.get(date_type, [])
        print(f"\n{date_type_names[date_type]}:")
        if hours_list:
            for i, period in enumerate(hours_list, 1):
                print(f"  {i}. {period['start_hour']}:{period['start_minute']:02d} - {period['end_hour']}:{period['end_minute']:02d}")
        else:
            print("  无")

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
    
    current_list = get_current_list()
    current_list.append(new_period)
    set_current_list(current_list)
    print(f"时间段已添加到 {date_type_names[current_date_type]}")

def edit_period():
    current_list = get_current_list()
    if not current_list:
        print("暂无时间段可编辑")
        return
    
    display_schedule()
    index = int(input("请输入要编辑的时间段编号: ")) - 1
    if 0 <= index < len(current_list):
        period = current_list[index]
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
        
        current_list[index] = updated_period
        set_current_list(current_list)
        print("时间段编辑成功")
    else:
        print("无效的时间段编号")

def delete_period():
    current_list = get_current_list()
    if not current_list:
        print("暂无时间段可删除")
        return
    
    display_schedule()
    index = int(input("请输入要删除的时间段编号: ")) - 1
    if 0 <= index < len(current_list):
        current_list.pop(index)
        set_current_list(current_list)
        print("时间段删除成功")
    else:
        print("无效的时间段编号")

def save():
    global modified
    if modified:
        config['restricted_hours'] = restricted_hours_dict
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
    global config, restricted_hours_dict, current_date_type
    try:
        config = load_config()
    except FileNotFoundError:
        print("配置文件不存在，请先运行 main.py 进行初始化")
        return
    
    restricted_hours_dict = config.get('restricted_hours', {}).copy()
    
    for key in ['workday', 'weekend', 'holiday']:
        if key not in restricted_hours_dict:
            restricted_hours_dict[key] = []
    
    print(f"当前编辑的是: {date_type_names[current_date_type]}")
    
    menu_items = {
        "切换日期类型": select_date_type,
        "查看当前日期类型的时间段": display_schedule,
        "查看所有日期类型的时间段": display_all_schedules,
        "添加新时间段": add_period,
        "编辑现有时间段": edit_period,
        "删除时间段": delete_period,
        "保存": save
    }
    
    menu = ConsoleMenu("时间段编辑器", menu_items)
    menu.execute()
    
    confirm_exit()

if __name__ == "__main__":
    main()