import os
import subprocess
import sys
import time

sys.path.append('./tools')  # 添加script目录到sys.path
from tools import printAndLog

formatted_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime())

# 设置视频的宽高和持续时间
resolution = "1080x1920"
duration = "1"  # 单位：秒


def add_empty_video(output_file, ffmpeg_path, cmd_log_level, work_path):
    try:
        # 构建FFmpeg命令
        ffmpeg_command = [
            ffmpeg_path,
            "-f", "lavfi",
            "-i", f"color=c=black:s={resolution}:d={duration}",
            "-c:v", "libx264",
            "-t", duration,
            "-pix_fmt", "yuv420p",
            output_file,
            "-loglevel", cmd_log_level,
        ]

        # print(f"Current working directory: {os.getcwd()}")

        # 执行FFmpeg命令，将工作目录设置为当前目录下的temp文件夹
        with open("logs/初始化-ffmpeg_output.log", "w") as log_file:
            subprocess.run(ffmpeg_command, stdout=log_file, stderr=log_file)

        video_path = os.path.join("temp", output_file)
        os.path.exists(video_path)

        log_file_path = "logs/"
        log_file_name = "初始化日志"

        printAndLog.log_and_print('初始化mp4文件已生成。', log_file_path, log_file_name)
    except Exception as e:
        printAndLog.log_and_print(e, "logs/", "初始化日志")


if __name__ == "__main__":
    output_file = "output_video.mp4"
    ffmpeg_path = "ffmpeg/bin/ffmpeg.exe"
    cmd_log_level = "debug"
    work_path = "temp/"
    add_empty_video(output_file, ffmpeg_path, cmd_log_level, work_path)
