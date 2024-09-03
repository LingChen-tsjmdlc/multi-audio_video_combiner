import subprocess
import os
import re
import sys
import time

import yaml

sys.path.append('./script')  # 添加script目录到sys.path
from script.tools import printAndLog


def convert_time_to_seconds(time_str):
    parts = time_str.split(':')
    hours = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds


def mixer(ffmpeg_path, video_path, audio_path, output_path, log_file_path, log_file_name, output_dir_with_no_audio, config_path):
    printAndLog.log_and_print("正在合并音频与视频……", log_file_path, log_file_name)
    # 添加了-loglevel debug选项来输出调试信息
    ffmpeg_command = f'{ffmpeg_path} -i "{output_dir_with_no_audio}" -i "{audio_path}" -c:v copy -c:a aac -strict experimental -loglevel verbose -progress - "{output_path}"'
    remove_audio_command = f'{ffmpeg_path} -i "{video_path}" -vcodec copy -an "{output_dir_with_no_audio}"'
    printAndLog.log_and_print(f"当前合并 ffmpeg 命令: {ffmpeg_command}", log_file_path, log_file_name, True)
    printAndLog.log_and_print(f"当前清除声道 ffmpeg 命令: {remove_audio_command}", log_file_path, log_file_name, True)
    if os.path.exists(output_path):
        os.remove(output_path)
        printAndLog.log_and_print(f"已存在的文件 '{output_path}' 已被替换。", log_file_path, log_file_name, True)


    try:
        if os.path.exists(output_dir_with_no_audio):    # 如果已经有临时的无音频的视频则删除
            os.remove(output_dir_with_no_audio)
        # 添加处理速度的正则表达式
        speed_pattern = re.compile(r"speed=\S+")
        frame_pattern = re.compile(r"frame=\s*(\d+)")

        # 总帧数
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        video_time = config['video_time']
        farm_output = config['farm_output']
        total_frames = video_time * farm_output

        printAndLog.log_and_print("\ni. 正在去除视频中空白轨道音频……", log_file_path, log_file_name)
        try:
            process = subprocess.Popen(remove_audio_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            # 实时打印ffmpeg的输出
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                printAndLog.log_and_print(f"{line.strip()}", log_file_path, log_file_name, True)
                frame_match = frame_pattern.search(line)
                if frame_match:
                    current_frame = int(frame_match.group(1))
                    # 计算进度
                    progress = (current_frame / total_frames) * 100
                    print(f"\r当前进度: {progress:.2f}%", end='', flush=True)

            process.wait()
            if process.returncode == 0:
                printAndLog.log_and_print("\n去除视频中空白音频轨道成功！", log_file_path, log_file_name)
            else:
                printAndLog.log_and_print(f"去除视频中空白音频轨道过程中发生错误，退出码: {process.returncode}", log_file_path,
                                          log_file_name)
                sys.exit()

        except Exception as e:
            printAndLog.log_and_print(f"去除空白音频报错：{e}", log_file_path, log_file_name)
            sys.exit()
        printAndLog.log_and_print("\nii. 正在合并视频和新的音频……", log_file_path, log_file_name)
        try:
            process = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        except Exception as e:
            printAndLog.log_and_print(f"合并noneAudio视频和音频失败:{e}", log_file_path, log_file_name)
            sys.exit()

        time_pattern = re.compile(r"out_time=(\S+)")
        size_pattern = re.compile(r"total_size=(\S+)")

        total_size = None
        last_time = None

        while True:
            line = process.stdout.readline()
            if not line:
                break
            printAndLog.log_and_print(f"{line.strip()}", log_file_path, log_file_name, True)

            # speed_match = speed_pattern.search(line)    # 匹配处理速度
            # if speed_match:
            #     speed_info = speed_match.group(0)
            #     print(f"\r当前处理速度: {speed_info}", end='', flush=True)
            frame_match = frame_pattern.search(line)    # 匹配处理进度
            if frame_match:
                current_frame = int(frame_match.group(1))
                progress = (current_frame / total_frames) * 100
                print(f"\r当前进度: {progress:.2f}%", end='', flush=True)

        process.wait()
        if process.returncode == 0:
            printAndLog.log_and_print(f"\n视频和音频合并成功！", log_file_path, log_file_name)
            # printAndLog.log_and_print("当前进度 100%\n", log_file_path, log_file_name)
            if os.path.exists(output_dir_with_no_audio):    # 删除临时的无音频的视频
                os.remove(output_dir_with_no_audio)
        else:
            printAndLog.log_and_print(f"合并过程中发生错误，退出码: {process.returncode}\n\n\n\n\n", log_file_path,
                                      log_file_name)

    except subprocess.CalledProcessError as e:
        printAndLog.log_and_print(f"未知错误！合并过程中发生错误: {e}\n\n\n\n\n", log_file_path, log_file_name)


if __name__ == "__main__":
    ffmpeg_dir = 'ffmpeg\\bin\\ffmpeg.exe'
    video_dir = 'temp/output_video.mp4'
    audio_dir = 'temp/output_audio.mp3'
    output_dir = '../Output/output_file-TEST.mp4'
    output_path_with_no_audio = 'temp/output_video-none_audio.mp4'
    log_file_dir = '../logs/'
    log_name = '混合视频音频日志'
    config_path = '../configs/config.yaml'
    mixer(ffmpeg_dir, video_dir, audio_dir, output_dir, log_file_dir, log_name, output_path_with_no_audio, config_path)
