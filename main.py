import os
import sys
import time
import logging
import yaml
import pprint

sys.path.append('./script')  # 添加script目录到sys.path
from script.tools import printAndLog

ffmpeg_dir = 'script\\ffmpeg\\bin\\ffmpeg.exe'
config_dir = 'configs/config.yaml'
output_video_dir = 'script/temp/output_video.mp4'
output_dir = 'Output/output_file.mp4'
log_dir = 'logs'
json_dir = 'script/temp/output.json'

try:
    now_time = time.strftime('%Y-%m-%d_%H-%M-%S')
    log_name = f'主日志_{now_time}'

    with open(config_dir, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    printAndLog.log_and_print(f"---> 当前config：{config}", log_dir, log_name, True)
    audio_file_format = config['audio_file_format']
    output_audio_dir = f"script/temp/output_audio.{audio_file_format}"

    if os.path.exists(f'script/temp/output_audio.{audio_file_format}'):
        os.remove(f'script/temp/output_audio.{audio_file_format}')

    from script import VideoMix
    from script import getVideoTime
    from script import getAudioStartTimeAndName
    from script import AudioMix
    from script import Mixer

    # 序列帧转视频
    printAndLog.log_and_print("<-------------------- 【1.序列帧转视频】(VideoMix.py) -------------------->", log_dir, log_name)
    VideoMix.video_mix(ffmpeg_dir, config_dir, output_video_dir, log_dir, log_name)
    # 获取视频时长
    printAndLog.log_and_print("<-------------------- 【2.获取视频时长】(getVideoTime.py) -------------------->", log_dir, log_name)
    getVideoTime.get_video_time(output_video_dir, ffmpeg_dir, config_dir, log_dir, log_name)
    # 获取工程文件中的音频信息和时间信息
    printAndLog.log_and_print("<-------------------- 【3.获取音频时间信息】(getAudioStartTimeAndName.py) -------------------->", log_dir, log_name)
    getAudioStartTimeAndName.get_audio_start_time_and_name(config_dir, json_dir, log_dir, log_name,audio_file_format)
    # 混合音频
    printAndLog.log_and_print("<-------------------- 【4.混合音频】(AudioMix.py) -------------------->", log_dir, log_name)
    AudioMix.audio_mix(config_dir, json_dir, output_audio_dir, log_dir, log_name)
    # 混合视频
    printAndLog.log_and_print("<-------------------- 【5.混合视频】(Mixer.py) -------------------->", log_dir, log_name)
    Mixer.mixer(ffmpeg_dir, output_video_dir, output_audio_dir, output_dir, log_dir, log_name)

    printAndLog.log_and_print("程序已结束。\n视频在Output文件夹下。\n按任意键结束程序...", log_dir, log_name)
    # 关闭日志记录器
    logging.shutdown()
except Exception as e:
    now_time = time.strftime('%Y-%m-%d_%H-%M-%S')
    printAndLog.log_and_print(f"未知错误！！！{e}", log_dir, f'主日志_{now_time}')
