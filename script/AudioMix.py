import os
import re
import subprocess
import sys
import yaml
import json
from pydub import AudioSegment

sys.path.append('./tools')  # 添加script目录到sys.path
from tools import printAndLog


def audio_mix(config_path, json_path, output_audio_path, log_file_path, log_file_name):
    try:
        # 读取配置文件
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        total_time = config['video_time']
        def_farm = config['def_farm']  # 视频每秒帧数
        audio_dir = config.get('audio_dir', '')  # 尝试获取audio_dir，如果不存在则默认为空字符串
        default_audio_dir = config['default_audio_dir']  # 音频文件默认目录
        audio_format = config['audio_file_format']

        # 根据audio_dir是否为空来选择使用的目录
        audio_directory = audio_dir if audio_dir else default_audio_dir

        # 读取JSON文件
        with open(json_path, 'r', encoding='utf-8') as json_file:
            audio_events = json.load(json_file)

        # 创建总音频轨道，预设为总视频时间长度的静音
        total_length = total_time * 1000
        total_audio = AudioSegment.silent(duration=total_length)

        # 遍历音频事件，加载并合并音频
        for event in audio_events:
            audio_filename = event['SoundEventName']  # 音频文件名
            start_frame = int(event['StartTime'])  # 将字符串转换为整数
            # 将帧数转换为毫秒（1秒 = def_farm，1帧 = 1000ms/def_farm）
            start_time = int((start_frame / def_farm) * 1000)
            audio_path = os.path.join(audio_directory, audio_filename)  # 完整音频路径
            audio_path = audio_path.replace('/', '\\')  # 替换正斜杠为反斜杠
            printAndLog.log_and_print(f"音频:{audio_path}", log_file_path, log_file_name,True)

            if not os.path.exists(audio_path):
                printAndLog.log_and_print(f"音频{audio_path}未找到", log_file_path, log_file_name)
                sys.exit()
                # print(f"Audio file {audio_path} not found. Skipping.")
                # continue  # Skip this audio file and continue with the next one

            try:
                audio = AudioSegment.from_file(audio_path)
                total_audio = total_audio.overlay(audio, position=start_time)
            except Exception as e:
                printAndLog.log_and_print(f"未知错误！音频路径{audio_path}：{e}", log_file_path, log_file_name)
                # print(f"Error processing audio file {audio_path}: {audio_path}")
                continue  # Skip this audio file and continue with the next one

        # 如果输出路径已存在，则删除
        if os.path.exists(output_audio_path):
            os.remove(output_audio_path)

        # 导出合并后的音频文件
        total_audio.export(output_audio_path, format=audio_format)
        printAndLog.log_and_print("合并音频成功！", log_file_path, log_file_name)
    except Exception as e:
        printAndLog.log_and_print(f"合并音频未知错误！{e}", log_file_path, log_file_name)


if __name__ == "__main__":
    config_dir = '../configs/config.yaml'
    json_dir = 'temp/output.json'
    with open(config_dir, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    audio_file_format = config['audio_file_format']
    output_audio_dir = f"temp/output_audio.{audio_file_format}"
    log_file_dir = "../logs/"
    log_name = "混合音频日志"
    # 调用audio_mix函数
    audio_mix(config_dir, json_dir, output_audio_dir, log_file_dir, log_name)
