import os
import sys
import time
import logging
import yaml

sys.path.append('./script')  # 添加script目录到sys.path

'''<--- 日志输出相关 --->'''
# 从config.yaml文件中读取配置信息
with open('configs/config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)
# 设置日志文件名
base_log_filename = '日志'
# 设置日志文件名，包含时间戳
log_filename = f"{base_log_filename}_{time.strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_filename = os.path.join('logs/', log_filename)
# 创建日志记录器，设置级别为DEBUG
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# 添加控制台输出处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)
# 输出配置信息到日志文件
logging.info(f"---> config：{config}")

if os.path.exists('script/temp/output_audio.wav'):
    os.remove('script/temp/output_audio.wav')

# from script import editConfig
from script import VideoMix
# from script import VideoMixExceedOneW
from script import getVideoTime
from script import getAudioStartTimeAndName
from script import AudioMix
from script import Mixer

render_dir = config['render_dir']
render_number = len(os.listdir(render_dir))

VideoMix.video_mix()
getVideoTime.get_video_time()
getAudioStartTimeAndName.get_audio_start_time_and_name()
AudioMix.audio_mix()
Mixer.mixer()

input("已结束。视频在Output文件夹下。按任意键结束程序...")
# 关闭日志记录器
logging.shutdown()
