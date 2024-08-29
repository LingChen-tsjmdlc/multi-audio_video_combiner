import subprocess
import os
import re

import yaml

ffmpeg_path = os.path.join('script', 'ffmpeg', 'bin', 'ffmpeg.exe')
config_path = os.path.join('configs', 'config.yaml')
if __name__ == "__main__":
    config_path = os.path.join('..', 'configs', 'config.yaml')
output_video = os.path.join('script/temp/output_video2.mp4')
log_dir = os.path.join('script/logs')  # 日志文件目录

# 读取config
with open(config_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)
farm_output = str(config['farm_output'])
render_dir = config['render_dir']

# 确保日志目录存在
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

ffmpeg_command = [
    ffmpeg_path,
    '-r', farm_output,
    '-f', 'image2',
    '-i', f'{render_dir}/%05d.png',
    '-crf', '15',
    output_video
]


def get_render_number():
    render_number = len(os.listdir(f'{render_dir}'))
    return render_number


def get_log_file_path(output_video):
    # 从输出视频路径中获取文件名
    log_filename = os.path.basename(output_video) + '.log'
    # 构建日志文件的完整路径
    log_file_path = os.path.join(log_dir, log_filename)
    return log_file_path


def parse_progress(line):
    match = re.search(r"frame=\s*(\d+)", line)
    if match:
        frame_number = int(match.group(1))
        return frame_number
    return None


def mix_video(ffmpeg_cmd):
    try:
        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, encoding='utf-8')

        total_frames = get_render_number()
        current_frame = 0

        log_file_path = get_log_file_path(output_video)
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                log_file.write(line)
                log_file.flush()

                frame = parse_progress(line)
                if frame is not None:
                    current_frame = frame
                    progress = (current_frame / total_frames) * 100
                    print(f'\r当前进度: {progress:.2f}%', end='')

        process.wait()
        if process.returncode == 0:
            print("\n当前进度：100%")
            print(f'临时视频已成功创建，目录: {output_video}')
        else:
            print(f'\n创建视频时出错，退出码: {process.returncode}')
    except subprocess.CalledProcessError as e:
        print(f'创建视频时出错: {e}')
        print(f'ffmpeg 命令: {ffmpeg_cmd}')
    except FileNotFoundError as e:
        print(f'找不到文件: {e}')
        print(f'ffmpeg 命令: {ffmpeg_cmd}')


def video_mix():
    print(f"合并视频前的config-inFile:{config}")
    print("合并视频中……")
    # 检查输出视频文件是否存在，如果存在则删除
    if os.path.exists(output_video):
        print("已经有相同临时视频，已经行替换！")
        os.remove(output_video)

    mix_video(ffmpeg_command)


if __name__ == "__main__":
    video_mix()