import os
import shutil
import sys
import time
import logging
import yaml

sys.path.append('./script')  # 添加script目录到sys.path
from script.tools import printAndLog

ffmpeg_dir = 'script\\ffmpeg\\bin\\ffmpeg.exe'
config_dir = 'configs/config.yaml'
output_video_dir = 'script/temp/output_video.mp4'
output_dir = 'Output/output_file.mp4'
log_dir = 'logs'
json_dir = 'script/temp/output.json'

try:
    now_time = time.strftime('%Y-%m-%d_%H-%M-%S')
    log_name = f'主日志_{now_time}'

    printAndLog.log_and_print(f"选择模式：\n1. 合并序列帧并对轨音频\n2. 仅对轨音频", log_dir, log_name)
    mode_choose = input("")
    while True:
        if mode_choose == "1":
            printAndLog.log_and_print(f"当前用户选择的是：{mode_choose}模式", log_dir, log_name, True)
            break
        if mode_choose == "2":
            print("------ 目前视频格式仅支持mp4 ------")
            printAndLog.log_and_print(f'0. 使用当前目录下的视频\n1. 使用默认视频输入路径（默认路径与序列帧路径相同）\n2. 使用指定路径', log_dir, log_name)
            is_default_dir = input()
            # 当前脚本所在的目录
            current_directory = os.path.dirname(os.path.abspath(__file__))

            if is_default_dir == '0':
                # 搜索当前目录下的所有mp4文件
                mp4_files = [f for f in os.listdir(current_directory) if f.lower().endswith('.mp4')]
                if len(mp4_files) > 1:
                    printAndLog.log_and_print(f"当前目录下存在多个MP4文件，请只保留一个文件。", log_dir, log_name)
                elif len(mp4_files) == 0:
                    printAndLog.log_and_print(f"当前目录下没有找到MP4文件，请确认路径或输入正确的文件路径。", log_dir,log_name)
                else:
                    printAndLog.log_and_print(f"当前目录下找到了{mp4_files[0]}", log_dir,log_name)
                    v_name = mp4_files[0]
                    v_dir = os.path.join(current_directory, v_name)
                    new_v_name = "output_video.mp4"
                    new_v_dir = os.path.join(current_directory, "script", "temp", new_v_name)
                    # 检查目标路径是否存在并删除已存在的文件
                    if os.path.exists(new_v_dir):
                        os.remove(new_v_dir)
                    # 重命名并移动视频文件
                    os.rename(v_dir, new_v_dir)
                    printAndLog.log_and_print(f"视频文件已重命名为：{new_v_name} 并移动到 script/temp 目录下。", log_dir,log_name)
                    break

            if is_default_dir == '1':
                with open(config_dir, 'r', encoding='utf-8') as file:
                    config = yaml.safe_load(file)
                render_dir = config['render_dir']
                # 搜索默认目录下的所有mp4文件
                mp4_files = [f for f in os.listdir(render_dir) if f.lower().endswith('.mp4')]
                if len(mp4_files) > 1:
                    printAndLog.log_and_print(f"默认目录下存在多个MP4文件，请只保留一个文件。", log_dir, log_name)
                elif len(mp4_files) == 0:
                    printAndLog.log_and_print(f"默认目录下没有找到MP4文件，请确认路径或输入正确的文件路径。", log_dir,log_name)
                else:
                    printAndLog.log_and_print(f"默认目录下找到了{mp4_files[0]}", log_dir,log_name)
                    v_name = mp4_files[0]
                    v_dir = os.path.join(render_dir, v_name)
                    new_v_name = "output_video.mp4"
                    new_v_dir = os.path.join(current_directory, "script", "temp", new_v_name)
                    # 检查目标路径是否存在并删除已存在的文件
                    if os.path.exists(new_v_dir):
                        os.remove(new_v_dir)
                    # 重命名并复制视频文件
                    shutil.copy(v_dir, new_v_dir)
                    printAndLog.log_and_print(f"视频文件已重命名为：{new_v_name} 并复制到 script/temp 目录下。", log_dir,log_name)
                    break

            if is_default_dir == '2':
                printAndLog.log_and_print(f'请输入视频的路径：', log_dir, log_name)
                v_path = input()
                printAndLog.log_and_print(f'请输入视频的名称：', log_dir, log_name)
                v_name = input()
                v_dir = os.path.join(v_path,v_name)
                new_v_dir = os.path.join(current_directory, "script", "temp", "output_video.mp4")
                shutil.copy(v_dir, new_v_dir)
                printAndLog.log_and_print(f"当前用户输入的路径是：{v_dir}", log_dir, log_name, True)

                break
        else:
            printAndLog.log_and_print(f"当前用户输入的模式是：{mode_choose}", log_dir, log_name, True)
            printAndLog.log_and_print(f'不可以选择其他模式哦~', log_dir, log_name)
            input()
            # continue
            sys.exit()

    with open(config_dir, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    printAndLog.log_and_print(f"---> 当前config：{config}", log_dir, log_name, True)
    audio_file_format = config['audio_file_format']
    output_audio_dir = f"script/temp/output_audio.{audio_file_format}"

    if os.path.exists(f'script/temp/output_audio.{audio_file_format}'):
        os.remove(f'script/temp/output_audio.{audio_file_format}')

    from script import VideoMix
    from script import getVideoTime
    from script import getAudioStartTimeAndName
    from script import AudioMix
    from script import Mixer

    # 序列帧转视频
    printAndLog.log_and_print("<-------------------- 【1.序列帧转视频】(VideoMix.py) -------------------->", log_dir, log_name)
    if mode_choose == "1":
        VideoMix.video_mix(ffmpeg_dir, config_dir, output_video_dir, log_dir, log_name)
    # 获取视频时长
    printAndLog.log_and_print("<-------------------- 【2.获取视频时长】(getVideoTime.py) -------------------->", log_dir, log_name)
    getVideoTime.get_video_time(output_video_dir, ffmpeg_dir, config_dir, log_dir, log_name)
    # 获取工程文件中的音频信息和时间信息
    printAndLog.log_and_print("<-------------------- 【3.获取音频时间信息】(getAudioStartTimeAndName.py) -------------------->", log_dir, log_name)
    getAudioStartTimeAndName.get_audio_start_time_and_name(config_dir, json_dir, log_dir, log_name,audio_file_format)
    # 混合音频
    printAndLog.log_and_print("<-------------------- 【4.混合音频】(AudioMix.py) -------------------->", log_dir, log_name)
    AudioMix.audio_mix(config_dir, json_dir, output_audio_dir, log_dir, log_name)
    # 混合视频
    printAndLog.log_and_print("<-------------------- 【5.混合视频】(Mixer.py) -------------------->", log_dir, log_name)
    Mixer.mixer(ffmpeg_dir, output_video_dir, output_audio_dir, output_dir, log_dir, log_name)

    printAndLog.log_and_print("程序已结束。\n视频在Output文件夹下。\n按任意键结束程序...", log_dir, log_name)
    # 关闭日志记录器
    logging.shutdown()
except Exception as e:
    now_time = time.strftime('%Y-%m-%d_%H-%M-%S')
    printAndLog.log_and_print(f"未知错误！！！{e}", log_dir, f'主日志_{now_time}')
