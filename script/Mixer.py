import subprocess
import os
import re

# 视频和音频文件的路径
video_file = 'script/temp/output_video.mp4'
audio_file = 'script/temp/output_audio.wav'

# 合并后的文件输出路径
output_file = 'Output/output_file.mp4'

# ffmpeg命令，添加了-progress选项来输出进度信息
ffmpeg_command = f'ffmpeg -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac -strict experimental -progress - "{output_file}"'


def convert_time_to_seconds(time_str):
    parts = time_str.split(':')
    hours = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds


def mixer():
    print("正在合并音频与视频")

    # 检查输出文件是否存在
    if os.path.exists(output_file):
        # 如果文件存在，可以选择删除或重命名
        os.remove(output_file)
        print(f"已存在的文件 '{output_file}' 已被替换。")

    # 执行命令
    try:
        # 使用subprocess.Popen而不是subprocess.run，以便实时获取输出
        process = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # 正则表达式来匹配ffmpeg进度输出
        time_pattern = re.compile(r"out_time=(\S+)")
        size_pattern = re.compile(r"total_size=(\S+)")

        # 初始化变量
        total_size = None
        last_time = None

        # 读取ffmpeg的输出
        while True:
            line = process.stdout.readline()
            if not line:
                break

            # 查找total_size
            size_match = size_pattern.search(line)
            if size_match:
                total_size = float(size_match.group(1))

            # 查找out_time
            time_match = time_pattern.search(line)
            if time_match:
                current_time = time_match.group(1)
                if total_size and current_time != last_time:
                    # 将时间字符串转换为秒
                    current_seconds = convert_time_to_seconds(current_time)
                    # 计算进度
                    progress = current_seconds / total_size * 100
                    print(f"当前进度: {progress:.2f}%")
                    last_time = current_time

        # 等待ffmpeg命令执行完成
        process.wait()

        if process.returncode == 0:
            print("视频和音频合并成功！")
        else:
            print(f"合并过程中发生错误，退出码: {process.returncode}")

    except subprocess.CalledProcessError as e:
        print(f"合并过程中发生错误: {e}")


if __name__ == "__main__":
    mixer()
