import datetime
import subprocess
import os
import sys

import yaml

sys.path.append('./script')  # 添加script目录到sys.path
from script.tools import printAndLog


def get_video_duration_ffmpeg(video_path, ffmpeg_bin_path,log_file_path, log_file_name):
    try:
        # 使用ffmpeg命令获取视频时长
        result = subprocess.run(
            [ffmpeg_bin_path, "-i", video_path, "-hide_banner"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # 搜索输出中包含视频时长的行
        output = result.stderr.decode()
        duration_lines = [line for line in output.splitlines() if "Duration" in line]
        if not duration_lines:
            printAndLog.log_and_print("没有找到包含'Duration'的行\n", log_file_path, log_file_name)
            return None
        duration_line = duration_lines[0]
        # 提取时长字符串
        duration_str = duration_line.split(",")[0].split("Duration:")[1].strip()
        # 将时长字符串转换为秒
        duration_parts = duration_str.split(':')
        duration_in_seconds = int(duration_parts[0]) * 3600 + int(duration_parts[1]) * 60 + float(duration_parts[2])
        return duration_in_seconds
    except subprocess.CalledProcessError as e:
        printAndLog.log_and_print(f"ffmpeg命令执行失败：{e}\n", log_file_path, log_file_name)
        return None


def get_video_time(video_path, ffmpeg_path, config_path,log_file_path, log_file_name):
    try:
        if not os.path.exists(ffmpeg_path):
            printAndLog.log_and_print(f"ffmpeg路径错误，无法找到文件：{ffmpeg_path}\n", log_file_path, log_file_name)
            exit(1)  # 退出程序
        total_time = get_video_duration_ffmpeg(video_path, ffmpeg_path,log_file_path, log_file_name)
        if total_time is not None:
            if total_time != 0:
                with open(config_path, 'r', encoding='utf-8') as file:
                    config = yaml.safe_load(file)
                config['video_time'] = total_time
                # 将更新后的配置写回文件
                with open(config_path, 'w', encoding='utf-8') as file:
                    yaml.dump(config, file, allow_unicode=True, sort_keys=False)
                printAndLog.log_and_print(f"视频时长：{total_time}秒\n", log_file_path, log_file_name)
            else:
                printAndLog.log_and_print("视频时长为0秒！出现错误！\n", log_file_path, log_file_name)
        else:
            printAndLog.log_and_print("无法获取视频时长\n", log_file_path, log_file_name)
    except Exception as e:
        printAndLog.log_and_print(f"发生未知错误：{e}\n", log_file_path, log_file_name)


if __name__ == "__main__":
    # 添加当前时间
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    video_dir = 'temp/output_video.mp4'
    ffmpeg_dir = os.path.join('ffmpeg', 'bin', 'ffmpeg.exe')
    config_dir = '../configs/config.yaml'
    log_file_dir = '../logs/'
    log_name = '日志.log'
    printAndLog.log_and_print(f"<----- {current_time} ----->", log_file_dir, log_name)
    # 调用函数并打印视频时长
    get_video_time(video_dir, ffmpeg_dir, config_dir,log_file_dir, log_name)
