#!/usr/bin/env python3
import os
import json

CONFIG_FILE = os.environ.get('CURFEW_CONFIG', os.path.join(os.getcwd(), 'config.json'))

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        restricted_hours = config.get('restricted_hours', {})
        
        for key in ['workday', 'weekend', 'holiday']:
            if key not in restricted_hours:
                restricted_hours[key] = []

        if 'continuous_usage_limits' not in config:
            config['continuous_usage_limits'] = {}
        for key in ['workday', 'weekend', 'holiday']:
            if key not in config['continuous_usage_limits']:
                config['continuous_usage_limits'][key] = 0

        return config
    
    raise FileNotFoundError("配置文件不存在，请先运行 main.py 进行配置")

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)