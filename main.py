import os
import subprocess
import sys
import time

import yaml

sys.path.append('./script')  # 添加script目录到sys.path

if os.path.exists('script/temp/output_audio.wav'):
    os.remove('script/temp/output_audio.wav')

# from script import editConfig
from script import VideoMix
from script import VideoMixExceedOneW
from script import getVideoTime
from script import getAudioStartTimeAndName
from script import AudioMix
from script import Mixer

# editConfig.edit_config()

# 在修改配置前先读取一次配置文件
with open('configs/config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)
print("合并视频前的config：", config)
# farm_output = config['farm_output']
render_dir = config['render_dir']
render_number = len(os.listdir(render_dir))
# time.sleep(10)

VideoMix.video_mix()
# if render_number >= 10000:
#     print("大于10000帧辣！请耐心等待……")
#     VideoMixExceedOneW.video_mix()
#     # output_video_path = 'script/temp/output_video.mp4'
#     # new_output_video_path = 'script/temp/output_video1.mp4'
#     # if os.path.exists(output_video_path):
#     #     os.rename(output_video_path, new_output_video_path)
#
#     video1_path = 'script/temp/output_video.mp4'
#     video2_path = 'script/temp/output_video2.mp4'
#     output_video_path = 'script/temp/output_video.mp4'
#     # 创建一个临时文本文件，用于存储视频文件的路径
#     concat_list_path = 'script/temp/concat_list.txt'
#     with open(concat_list_path, 'w') as f:
#         f.write(f"file '{video1_path}'\n")
#         f.write(f"file '{video2_path}'\n")
#     # 构建ffmpeg命令
#     ffmpeg_command = [
#         'ffmpeg',
#         '-f', 'concat',  # 指定输入文件格式为concat
#         '-safe', '0',  # 禁用文件名中的安全检查
#         '-i', concat_list_path,  # 输入文件列表
#         '-c', 'copy',  # 直接复制流，不重新编码
#         output_video_path  # 输出视频文件
#     ]
#     # 执行ffmpeg命令
#     subprocess.run(ffmpeg_command)
#     # 删除临时文本文件
#     os.remove(concat_list_path)

getVideoTime.get_video_time()
getAudioStartTimeAndName.get_audio_start_time_and_name()
AudioMix.audio_mix()
Mixer.mixer()

input("已结束。视频在Output文件夹下。回车退出程序")
