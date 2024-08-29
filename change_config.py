import os
import sys

sys.path.append('./script')  # 添加script目录到sys.path

from script import editConfig
editConfig.edit_config()

if os.path.exists('script/temp/output_audio.wav'):
    os.remove('script/temp/output_audio.wav')
input("已结束。回车退出程序")