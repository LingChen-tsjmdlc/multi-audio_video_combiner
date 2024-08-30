import os
import sys

sys.path.append('./script')  # 添加script目录到sys.path

from script import editConfig


# 修改 config 文件
config_path = "configs/config.yaml"
editConfig.edit_config(config_path)

input("已结束。回车退出程序")
