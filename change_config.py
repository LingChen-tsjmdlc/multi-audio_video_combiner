import os
import sys
import time

sys.path.append('./script')  # 添加script目录到sys.path
from script.tools import printAndLog
from script import editConfig

log_dir = 'logs'
now_time = time.strftime('%Y-%m-%d_%H-%M-%S')
log_name = f'日志-配置初始化_{now_time}'
config_path = "configs/config.yaml"

# 修改 config 文件
printAndLog.log_and_print(f"<-------------------- 【0.修改配置文件】(editConfig.py) -------------------->", log_dir, log_name)
editConfig.edit_config(config_path, log_dir, log_name)


input("已结束。回车退出程序")
