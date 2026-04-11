#!/usr/bin/env python3
from config import load_config, save_config

def display_menu():
    print("\n===== 时间段编辑器 =====")
    print("1. 查看当前时间段列表")
    print("2. 添加新时间段")
    print("3. 编辑现有时间段")
    print("4. 删除时间段")
    print("5. 保存并退出")
    print("6. 放弃修改并退出")
    choice = input("请输入选项编号: ")
    return choice

def display_schedule(restricted_hours_list):
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
    
    return {
        'start_hour': start_hour,
        'start_minute': start_minute,
        'end_hour': end_hour,
        'end_minute': end_minute
    }

def edit_period(period):
    print("\n编辑时间段:")
    print(f"当前时间: {period['start_hour']}:{period['start_minute']:02d} - {period['end_hour']}:{period['end_minute']:02d}")
    
    start_hour = int(input(f"开始小时 (0-23) [默认: {period['start_hour']}]: ") or period['start_hour'])
    start_minute = int(input(f"开始分钟 (0-59) [默认: {period['start_minute']}]: ") or period['start_minute'])
    end_hour = int(input(f"结束小时 (0-23) [默认: {period['end_hour']}]: ") or period['end_hour'])
    end_minute = int(input(f"结束分钟 (0-59) [默认: {period['end_minute']}]: ") or period['end_minute'])
    
    return {
        'start_hour': start_hour,
        'start_minute': start_minute,
        'end_hour': end_hour,
        'end_minute': end_minute
    }

def main():
    try:
        config = load_config()
    except FileNotFoundError:
        print("配置文件不存在，请先运行 main.py 进行初始化")
        return
    
    # 获取并标准化时间段列表
    restricted_hours_list = config.get('restricted_hours', [])
    if isinstance(restricted_hours_list, dict):
        restricted_hours_list = [restricted_hours_list]
    
    modified = False
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            display_schedule(restricted_hours_list)
        elif choice == '2':
            new_period = add_period()
            restricted_hours_list.append(new_period)
            modified = True
            print("时间段添加成功")
        elif choice == '3':
            if not restricted_hours_list:
                print("暂无时间段可编辑")
                continue
            
            display_schedule(restricted_hours_list)
            index = int(input("请输入要编辑的时间段编号: ")) - 1
            if 0 <= index < len(restricted_hours_list):
                updated_period = edit_period(restricted_hours_list[index])
                restricted_hours_list[index] = updated_period
                modified = True
                print("时间段编辑成功")
            else:
                print("无效的时间段编号")
        elif choice == '4':
            if not restricted_hours_list:
                print("暂无时间段可删除")
                continue
            
            display_schedule(restricted_hours_list)
            index = int(input("请输入要删除的时间段编号: ")) - 1
            if 0 <= index < len(restricted_hours_list):
                restricted_hours_list.pop(index)
                modified = True
                print("时间段删除成功")
            else:
                print("无效的时间段编号")
        elif choice == '5':
            if modified:
                config['restricted_hours'] = restricted_hours_list
                save_config(config)
                print("配置已保存")
            print("退出编辑器")
            break
        elif choice == '6':
            if modified:
                confirm = input("有未保存的修改，确定要放弃吗？(y/n): ")
                if confirm.lower() != 'y':
                    continue
            print("退出编辑器")
            break
        else:
            print("无效的选项，请重新输入")

if __name__ == "__main__":
    main()