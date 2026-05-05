![Stone Badge](https://stone.professorlee.work/api/stone/alu-deak/Curfew)

网络上说说就得了，现实中谁不想急头白脸的在readme里养一只石墩子做宠物（

# Curfew - 让时间管理更智能，让生活更有规律。

Curfew 是一个智能的开机启动工具，帮助您管理电脑的使用时间，在设定的禁用时段自动执行关机操作。

> [!IMPORTANT]
> 作者使用Linux系统，因此对Windows系统的支持可能有限，且仅在Linux环境下测试。
>
> 这是一个不负责任的作者，因为已知的用户只有作者自己。请自行解决旧版兼容性问题。\
> 升级前请务必做好配置备份，如有问题请自行调试。

## 📖 使用场景

- 限制自己使用电脑的时间，培养良好的时间管理习惯，避免沉迷于电脑

## 🚀 快速开始

### 1. 创建虚拟环境

在项目目录中创建名为 .venv 的虚拟环境：

```bash
python3 -m venv .venv
```

### 2. 安装依赖

激活虚拟环境并安装项目所需的依赖：

#### Linux/macOS

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. 首次配置

激活虚拟环境并运行配置向导，按照提示完成设置（需要管理员权限）：

#### Linux/macOS

```bash
sudo su
source .venv/bin/activate  # 先切到su用户，再激活环境，避免依赖无法加载
sudo python3 main.py # 初始化，创建配置文件，创建systemd服务文件
python3 app.py #启动GUI配置
```

配置过程中，您需要：

- 选择系统模式（Windows/Linux/自定义）
- 设置禁用时段（24小时制）
- 设置检测间隔（分钟）

### 4. 运行主程序

配置完成后，主程序会在开机时自动运行。您也可以手动启动：

#### Linux/macOS

```bash
source .venv/bin/activate
python3 curfew.py
```

程序会按照设置的检测间隔，持续检查当前时间是否在禁用时段内。

## ⚙️ 配置说明

### 调试模式

如需测试功能而不实际执行关机操作，可将 config.json 中的 "debug" 设置为 true 。

## 💡 小贴士

- **跨天设置**：支持跨天的禁用时段，如晚上 11 点到早上 7 点
- **权限要求**：设置 systemd 服务需要 root 权限
- **测试建议**：首次使用时，建议将 debug 设置为 true 进行测试
