import subprocess
import os
import yaml

# ffmpeg的路径
ffmpeg_path = os.path.join('script', 'ffmpeg', 'bin', 'ffmpeg.exe')

# 确认ffmpeg路径是否存在
if not os.path.exists(ffmpeg_path):
    print(f"ffmpeg路径错误，无法找到文件：{ffmpeg_path}")
    exit(1)  # 退出程序


def get_video_duration_ffmpeg(video_path, ffmpeg_bin_path):
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
        print("没有找到包含'Duration'的行")
        return None

    duration_line = duration_lines[0]

    # 提取时长字符串
    duration_str = duration_line.split(",")[0].split("Duration:")[1].strip()

    # 将时长字符串转换为秒
    duration_parts = duration_str.split(':')
    duration_in_seconds = int(duration_parts[0]) * 3600 + int(duration_parts[1]) * 60 + float(duration_parts[2])

    return duration_in_seconds


# 视频文件的路径
video_path = 'script/temp/output_video.mp4'


def get_video_time():
    total_time = get_video_duration_ffmpeg(video_path, ffmpeg_path)
    if total_time is not None:
        if total_time != 0:
            with open('configs/config.yaml', 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            config['video_time'] = total_time
            # 将更新后的配置写回文件
            with open('configs/config.yaml', 'w', encoding='utf-8') as file:
                yaml.dump(config, file, allow_unicode=True, sort_keys=False)
            print(f"视频时长：{total_time}秒")
        else:
            input("视频时长为0秒！出现错误！")
    else:
        print("无法获取视频时长")


if __name__ == "__main__":
    # 调用函数并打印视频时长
    get_video_time()
