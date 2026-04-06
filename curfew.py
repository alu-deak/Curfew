#!/usr/bin/env python3
import time
import logging
import signal
from config import load_config
from time_check import is_in_restricted_hours
from shutdown import shutdown

# 配置日志
import os
log_file = os.path.join(os.getcwd(), 'curfew.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 全局变量，用于控制循环
running = True

def signal_handler(signum, frame):
    """处理信号，优雅退出"""
    global running
    logger.info(f"收到信号 {signum}，准备退出...")
    running = False

def main():
    # 加载配置
    config = load_config()
    
    if not config:
        logger.error("未找到配置文件，请先运行 welcome.py 进行配置")
        return
    
    # 获取配置
    restricted = config['restricted_hours']
    check_interval = config.get('check_interval', 5)  # 默认5分钟
    debug = config.get('debug', False)
    
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("Curfew 启动，开始检测禁用时段")
    logger.info(f"禁用时段: {restricted['start_hour']}:{restricted['start_minute']:02d} - {restricted['end_hour']}:{restricted['end_minute']:02d}")
    logger.info(f"检测间隔: {check_interval} 分钟")
    
    global running
    while running:
        try:
            if is_in_restricted_hours(
                restricted['start_hour'],
                restricted['start_minute'],
                restricted['end_hour'],
                restricted['end_minute']
            ):
                logger.info("检测到当前时间在禁用时段内")
                # 根据 debug 配置决定是否在调试模式下运行
                if debug:
                    logger.info("调试模式，执行关机命令（模拟）")
                    shutdown(config['shutdown_command'], test_mode=True)
                else:
                    logger.info("执行关机命令")
                    shutdown(config['shutdown_command'])
                break
            else:
                logger.debug(f"当前时间不在禁用时段内，{check_interval}分钟后再次检测")
                # 睡眠指定的检测间隔
                for _ in range(check_interval * 60):
                    if not running:
                        break
                    time.sleep(1)
        except Exception as e:
            logger.error(f"检测过程中出现错误: {e}")
            # 出错后等待一段时间再重试
            time.sleep(60)
    
    logger.info("Curfew 退出")

if __name__ == "__main__":
    config = load_config()
    from daemon import DaemonContext
    with DaemonContext():
    main()