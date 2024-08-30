import os
import sys
import yaml
import re
import json

sys.path.append('./script')  # 添加script目录到sys.path
from script.tools import printAndLog


def get_audio_start_time_and_name(config_path, json_path, log_file_path, log_file_name):
    try:
        # 存储结果的列表
        results = []
        # 读取配置文件并获取movie_save_dir路径
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        movie_save_dir = config['movie_save_dir']  # 确保路径正确
        # 打开文件并读取内容
        with open(movie_save_dir, 'r', encoding='ansi') as file:
            content = file.read()

        # 使用正则表达式查找外部声音标签
        pattern = r'<Track Name="" Type="35" Category="外部声音">.*</Track>'
        matches = re.findall(pattern, content, re.DOTALL)

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
                    printAndLog.log_and_print(f'StartTime:{start_time}\tSoundEventName:{sound_event_name}', log_file_path,
                                              log_file_name)
                else:
                    results.append({
                        'StartTime': '未找到起始时间',
                        'SoundEventName': '未找到音频'
                    })
                    printAndLog.log_and_print('StartTime:未找到起始时间!\tSoundEventName:未找到音频!', log_file_path,
                                              log_file_name)
        printAndLog.log_and_print('\n', log_file_path, log_file_name)
        if os.path.exists(json_path):
            open(json_path, 'w').close()
        # 将结果转换为JSON格式并写入文件
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(results, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        printAndLog.log_and_print(f'未知错误！{e}', log_file_path,log_file_name)


if __name__ == "__main__":
    config_dir = '../configs/config.yaml'
    json_dir = 'temp/output.json'
    log_file_dir = '../logs/'
    log_file_name = '获取音频数据日志'
    get_audio_start_time_and_name(config_dir, json_dir, log_file_dir, log_file_name)
