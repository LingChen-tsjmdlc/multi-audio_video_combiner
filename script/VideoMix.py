import datetime
import subprocess
import os
import re
import sys

import yaml

sys.path.append('./script')  # 添加script目录到sys.path
from script.tools import printAndLog


def video_mix(ffmpeg_dir, config_dir, output_video_dir, log_dir, log_name):
    try:
        ffmpeg_path = ffmpeg_dir
        config_path = config_dir
        output_video = output_video_dir

        # 确保日志目录存在
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 读取config
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        farm_output = str(config['farm_output'])
        render_dir = config['render_dir']

        ffmpeg_command = [
            ffmpeg_path,
            '-r', farm_output,
            '-f', 'image2',
            '-i', f'{render_dir}/%04d.png',
            '-crf', '15',
            '-loglevel', 'info',
            output_video
        ]

        def get_render_number():
            render_number = len(os.listdir(f'{render_dir}'))
            return render_number

        def parse_progress(line):
            match = re.search(r"frame=\s*(\d+)", line)
            return int(match.group(1)) if match else None

        def mix_video(ffmpeg_cmd):
            process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, encoding='utf-8')
            total_frames = get_render_number()

            while True:
                line = process.stdout.readline()
                if not line:
                    break
                if line:
                    printAndLog.log_and_print(f"{line.strip()}", log_dir, log_name,True)
                # 使用 print 而不是 printAndLog.log_and_print 来更新进度
                frame = parse_progress(line)
                if frame is not None:
                    current_frame = frame
                    progress = (current_frame / total_frames) * 100
                    print(f'\r当前进度: {progress:.2f}%', end='', flush=True)  # 添加 flush=True 来确保立即刷新输出

            process.wait()
            # 确保在输出结果后换行
            print()
            if process.returncode == 0:
                printAndLog.log_and_print(f"当前进度：100%\n临时视频已成功创建，目录: {output_video}", log_dir, log_name)
            else:
                printAndLog.log_and_print(f"创建视频时出错，退出码: {process.returncode}\nffmpeg 命令: {ffmpeg_cmd}", log_dir, log_name)

        printAndLog.log_and_print(f"合并视频中……", log_dir, log_name)
        # 检查输出视频文件是否存在，如果存在则删除
        if os.path.exists(output_video):
            os.remove(output_video)

        mix_video(ffmpeg_command)
    except Exception as e:
        printAndLog.log_and_print(f"未知错误！{e}", log_dir, log_name)


if __name__ == "__main__":
    ffmpeg_dir = 'ffmpeg/bin/ffmpeg.exe'
    config_dir = '../configs/config.yaml'
    output_video_dir = 'temp/output_video.mp4'
    log_dir = '../logs'
    log_name = '序列帧转视频日志'
    video_mix(ffmpeg_dir, config_dir, output_video_dir, log_dir, log_name)
