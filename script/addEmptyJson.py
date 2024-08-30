import json
import sys
import time

sys.path.append('./tools')  # 添加script目录到sys.path
from tools import printAndLog

formatted_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime())

# 定义音频事件数据
temp_json_file = [
    {
        "StartTime": "0",
        "SoundEventName": "temp1.wav"
    },
    {
        "StartTime": "1",
        "SoundEventName": "temp2.wav"
    }
]


def add_empty_json_file(json_filename):
    try:
        # 将数据写入JSON文件
        with open(json_filename, 'w', encoding='utf-8') as file:
            json.dump(temp_json_file, file, ensure_ascii=False, indent=4)
        printAndLog.log_and_print('初始化Json文件已生成。', "logs/", "初始化日志")
    except Exception as e:
        printAndLog.log_and_print(e,"logs/","初始化日志")


if __name__ == "__main__":
    json_output_filename = 'temp/output.json'
    add_empty_json_file(json_output_filename)
