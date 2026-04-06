#!/usr/bin/env python3
import os
import json

CONFIG_FILE = os.path.join(os.getcwd(), 'config.json')

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    raise FileNotFoundError("配置文件不存在，请先运行 welcome.py 进行配置")

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
