#!/usr/bin/env python3
import os
import sys
import platform
import subprocess

def setup_autostart(autostart_type, script_path):
    if autostart_type == 'task scheduler':
        setup_task_scheduler(script_path)
    elif autostart_type == 'systemd':
        setup_systemd(script_path)
    else:
        print("请稍后自行设置自启动")

def setup_task_scheduler(script_path):
    if platform.system() == 'Windows':
        try:
            # 创建 Windows 计划任务
            task_name = "Curfew"
            # 构建虚拟环境激活脚本路径
            venv_activate = os.path.join(os.path.dirname(script_path), '.venv', 'Scripts', 'activate.bat')
            # 使用 schtasks 命令创建计划任务
            # /sc onstart 表示开机启动
            # /tn 任务名称
            # /tr 要执行的命令
            # /ru SYSTEM 以系统权限运行
            command = f"schtasks /create /sc onstart /tn {task_name} /tr \"cmd /c {venv_activate} && python {script_path}\" /ru SYSTEM"
            subprocess.run(command, shell=True, check=True)
            print("Windows 计划任务已设置")
        except Exception as e:
            print(f"设置 Windows 计划任务失败: {e}")
    else:
        print("Windows 计划任务仅在 Windows 系统上可用")

def setup_systemd(script_path):
    # 检查是否具有 root 权限
    if os.geteuid() != 0:
        print("需要root权限来创建systemd服务文件")
        return
    
    # 构建虚拟环境路径
    venv_path = os.path.join(os.path.dirname(script_path), '.venv')
    activate_script = os.path.join(venv_path, 'bin', 'activate')
    service_file = '/etc/systemd/system/curfew.service'
    service_content = f"""
[Unit]
Description=Curfew Service
After=network.target

[Service]
Type=simple
User=root
Environment=CURFEW_CONFIG={os.path.join(os.path.dirname(script_path), 'config.json')}
ExecStart=/bin/bash -c 'source {activate_script} && python3 {script_path}'
Restart=no

[Install]
WantedBy=multi-user.target
"""
    
    try:
        with open(service_file, 'w') as f:
            f.write(service_content)
        subprocess.run(['systemctl', 'daemon-reload'], check=True)
        subprocess.run(['systemctl', 'enable', 'curfew.service'], check=True)
        print("systemd 服务已设置")
    except Exception as e:
        print(f"设置 systemd 服务失败: {e}")
