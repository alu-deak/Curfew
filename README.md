# Curfew - 让时间管理更智能，让生活更有规律。

Curfew 是一个智能的开机启动工具，帮助您管理电脑的使用时间，在设定的禁用时段自动执行关机操作。

## 🎯 核心功能

- **智能时间管理**：设置禁用时段，自动检测并执行关机操作
- **跨平台支持**：同时支持 Windows 和 Linux 系统
- **灵活的自启动选项**：
  - Windows 系统：自动设置计划任务
  - Linux 系统：自动配置 systemd 服务
  - 自定义模式：根据需要自行设置
- **可调节的检测间隔**：根据您的需求设置检查时间间隔
- **安全的调试模式**：在测试时避免实际执行关机操作

## 📖 使用场景
限制自己使用电脑的时间，培养良好的时间管理习惯，避免沉迷于电脑

## 🚀 快速开始

### 1. 创建虚拟环境

在项目目录中创建名为 .venv 的虚拟环境：

```bash
# Linux/macOS
python3 -m venv .venv

# Windows
python -m venv .venv
```

### 2. 首次配置

激活虚拟环境并运行配置向导，按照提示完成设置（需要管理员权限）：

```bash
# Linux/macOS
source .venv/bin/activate
sudo python3 welcome.py

# Windows
.venv\Scripts\activate.bat
# 以管理员身份运行命令提示符，然后执行：
python welcome.py
```

配置过程中，您需要：
- 选择系统模式（Windows/Linux/自定义）
- 设置禁用时段（24小时制）
- 设置检测间隔（分钟）

### 3. 运行主程序

配置完成后，主程序会在开机时自动运行。您也可以手动启动：

```bash
# Linux/macOS
source .venv/bin/activate
python3 curfew.py

# Windows
.venv\Scripts\activate.bat
python curfew.py
```

程序会按照设置的检测间隔，持续检查当前时间是否在禁用时段内。

## ⚙️ 配置说明

配置文件 `config.json` 会在首次运行 `welcome.py` 后自动生成，包含以下设置：

```json
{
    "autostart_type": "systemd",  // 自启动类型
    "shutdown_command": ["shutdown", "now"],  // 关机命令
    "restricted_hours": [
        {
            "start_hour": 13,  // 禁用时段开始小时
            "start_minute": 30,  // 禁用时段开始分钟
            "end_hour": 17,  // 禁用时段结束小时
            "end_minute": 0  // 禁用时段结束分钟
        },
        {
            "start_hour": 23,  // 禁用时段开始小时
            "start_minute": 0,  // 禁用时段开始分钟
            "end_hour": 6,  // 禁用时段结束小时
            "end_minute": 0  // 禁用时段结束分钟
        }
    ],
    "check_interval": 5,  // 检测间隔（分钟）
    "debug": false  // 调试模式
}
```

### 调试模式

如需测试功能而不实际执行关机操作，可将 `debug` 设置为 `true`。

## 💡 小贴士

- **跨天设置**：支持跨天的禁用时段，如晚上 11 点到早上 7 点
- **权限要求**：设置 systemd 服务需要 root 权限
- **重新配置**：如需修改配置，删除 `config.json` 文件后再次运行 `welcome.py`
- **测试建议**：首次使用时，建议将 `debug` 设置为 `true` 进行测试