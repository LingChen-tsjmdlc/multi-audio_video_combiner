import subprocess
import os
import re
import sys
import time

sys.path.append('./script')  # 添加script目录到sys.path
from script.tools import printAndLog


def convert_time_to_seconds(time_str):
    parts = time_str.split(':')
    hours = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds


def mixer(video_path, audio_path, output_path, log_file_path, log_file_name):
    printAndLog.log_and_print("正在合并音频与视频……", log_file_path, log_file_name)
    # 添加了-loglevel debug选项来输出调试信息
    ffmpeg_command = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -strict experimental -loglevel verbose -progress - "{output_path}"'
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"已存在的文件 '{output_path}' 已被替换。")

    try:
        process = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True)

        time_pattern = re.compile(r"out_time=(\S+)")
        size_pattern = re.compile(r"total_size=(\S+)")

        total_size = None
        last_time = None

        while True:
            line = process.stdout.readline()
            if not line:
                break
            printAndLog.log_and_print(f"{line.strip()}", log_file_path, log_file_name,True)
            size_match = size_pattern.search(line)
            if size_match:
                total_size = float(size_match.group(1))
            time_match = time_pattern.search(line)
            if time_match:
                current_time = time_match.group(1)
                if total_size and current_time != last_time:
                    current_seconds = convert_time_to_seconds(current_time)
                    progress = current_seconds / total_size * 100
                    print(f"当前进度: {progress:.2f}%")
                    last_time = current_time
        process.wait()
        if process.returncode == 0:
            printAndLog.log_and_print(f"视频和音频合并成功！", log_file_path, log_file_name)
            printAndLog.log_and_print("当前进度 100%\n", log_file_path, log_file_name)
        else:
            printAndLog.log_and_print(f"合并过程中发生错误，退出码: {process.returncode}\n\n\n\n\n", log_file_path,
                                      log_file_name)

    except subprocess.CalledProcessError as e:
        printAndLog.log_and_print(f"未知错误！合并过程中发生错误: {e}\n\n\n\n\n", log_file_path, log_file_name)


if __name__ == "__main__":
    video_dir = 'temp/output_video.mp4'
    audio_dir = 'temp/output_audio.wav'
    output_dir = 'output_file.mp4'
    log_file_dir = '../logs/'
    log_name = '混合视频音频日志'
    mixer(video_dir, audio_dir, output_dir, log_file_dir, log_name)
