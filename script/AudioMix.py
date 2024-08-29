import os

import yaml
import json
from pydub import AudioSegment


def audio_mix():
    # 读取配置文件
    with open('configs/config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    total_time = config['video_time']
    def_farm = config['def_farm']  # 视频每秒帧数
    audio_dir = config.get('audio_dir', '')  # 尝试获取audio_dir，如果不存在则默认为空字符串
    default_audio_dir = config['default_audio_dir']  # 音频文件默认目录

    # 根据audio_dir是否为空来选择使用的目录
    audio_directory = audio_dir if audio_dir else default_audio_dir

    # 读取JSON文件
    with open('script/temp/output.json', 'r', encoding='utf-8') as json_file:
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
        audio_path = f"{audio_directory}/{audio_filename}"  # 完整音频路径
        try:
            audio = AudioSegment.from_file(audio_path)
            total_audio = total_audio.overlay(audio, position=start_time)
        except FileNotFoundError:
            print(f"Audio file {audio_path} not found. Skipping.")
    if os.path.exists('script/temp/output_audio.wav'):
        os.remove('script/temp/output_audio.wav')
    total_audio.export("script/temp/output_audio.wav", format="wav")


if __name__ == "__main__":
    # 读取配置文件
    with open('../configs/config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    total_time = config['video_time']
    def_farm = config['def_farm']  # 视频每秒帧数
    audio_dir = config.get('audio_dir', '')  # 尝试获取audio_dir，如果不存在则默认为空字符串
    default_audio_dir = config['default_audio_dir']  # 音频文件默认目录

    # 根据audio_dir是否为空来选择使用的目录
    audio_directory = audio_dir if audio_dir else default_audio_dir

    # 读取JSON文件
    with open('temp/output.json', 'r', encoding='utf-8') as json_file:
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
        audio_path = f"{audio_directory}/{audio_filename}"  # 完整音频路径
        try:
            audio = AudioSegment.from_file(audio_path)
            total_audio = total_audio.overlay(audio, position=start_time)
        except FileNotFoundError:
            print(f"Audio file {audio_path} not found. Skipping.")
    # 导出合并后的音频文件
    total_audio.export("temp/output_audio.wav", format="wav")
