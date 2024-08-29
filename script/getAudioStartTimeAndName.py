import os

import yaml
import re
import json


def get_audio_start_time_and_name():
    # 读取配置文件并获取movie_save_dir路径
    with open('configs/config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    movie_save_dir = config['movie_save_dir']  # 确保路径正确

    # 打开文件并读取内容
    with open(movie_save_dir, 'r', encoding='ansi') as file:
        content = file.read()

    # 使用正则表达式查找外部声音标签
    pattern = r'<Track Name="" Type="35" Category="外部声音">.*</Track>'
    matches = re.findall(pattern, content, re.DOTALL)

    # 存储结果的列表
    results = []

    # 输出找到的标签，并筛选StartTime和ExternalSoundEvent属性
    for track in matches:
        # 查找StartTime和ExternalSoundEvent
        start_time_pattern = r'StartTime="(\d+)"'
        external_sound_event_pattern = r'ExternalSoundEvent="([^"]+\.wav)"'

        start_time_matches = re.findall(start_time_pattern, track)
        external_sound_event_matches = re.findall(external_sound_event_pattern, track)

        # 处理并输出每个匹配项
        for start_time, external_sound_event in zip(start_time_matches, external_sound_event_matches):
            # 提取.wav前面的、\后面的文字
            sound_event_match = re.search(r'\\.*\.wav', external_sound_event)
            if sound_event_match:
                sound_event_name = sound_event_match.group()
                sound_event_name = sound_event_name.replace('\\', '/')
                pattern = r"/UserData/external_sound/"
                sound_event_name = re.sub(pattern, "", sound_event_name)
                results.append({
                    'StartTime': start_time,
                    'SoundEventName': sound_event_name
                })
            else:
                results.append({
                    'StartTime': '未找到起始时间',
                    'SoundEventName': '未找到音频'
                })
    if os.path.exists('script/temp/output.json'):
        open('script/temp/output.json', 'w').close()
    # 将结果转换为JSON格式并写入文件
    with open('script/temp/output.json', 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    get_audio_start_time_and_name()