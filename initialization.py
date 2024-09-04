import subprocess
import sys
import os
import time
import shutil

if getattr(sys, 'frozen', False):
    application_path = os.getcwd()  # 如果是打包后的程序
else:
    application_path = os.path.dirname(os.path.abspath(__file__))  # 如果是 非 打包后的程序

# 定义要创建的目录列表
directories_to_create = [
    os.path.join("script/ffmpeg/bin"),
    os.path.join("script/logs/"),
    os.path.join("script/temp/"),
    os.path.join("Output/"),
    os.path.join("logs/"),
    os.path.join("configs/"),
    os.path.join("script/tools")
]
# 检查每个目录是否存在，如果不存在则创建
print("\n<---------- 目录生成 ---------->")
for directory in directories_to_create:
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"已创建目录: {directory}")
        else:
            print(f"{directory}目录已存在")
    except Exception as e:
        print(f"创建目录失败: {directory}, 错误: {e}")

# 将根目录下的ffmpeg.exe移动到script/ffmpeg/bin目录
ffmpeg_source_path = os.path.join("ffmpeg.exe")
ffmpeg_destination_path = os.path.join("script/ffmpeg/bin/ffmpeg.exe")
if os.path.exists(ffmpeg_source_path):
    try:
        # 确保目标目录存在
        os.makedirs(os.path.dirname(ffmpeg_destination_path), exist_ok=True)

        if not os.path.exists(ffmpeg_destination_path):
            # 使用 shutil 模块进行复制
            shutil.copy(ffmpeg_source_path, ffmpeg_destination_path)
            print(f"ffmpeg.exe 已复制到 {ffmpeg_destination_path}")
        else:
            print(f"{ffmpeg_destination_path} 已存在，未复制 ffmpeg.exe")
    except Exception as e:
        print(f"复制 ffmpeg.exe 失败: {e}")
        input("初始化失败！")
        sys.exit()
else:
    print("ffmpeg.exe 可能不在根目录下！")
    input("初始化失败！")
    sys.exit()

# 移动 printAndLog.py
file_to_move = os.path.join("printAndLog.py")  # 定义要移动的文件路径
destination_directory = os.path.join("script/tools")  # 定义目标目录路径
if not os.path.exists(destination_directory):  # 检查目标目录是否存在，如果不存在则创建
    os.makedirs(destination_directory)
try:  # 尝试移动文件
    if os.path.exists(file_to_move):
        os.rename(file_to_move, os.path.join(destination_directory, os.path.basename(file_to_move)))
        print(f"文件已成功移动到 {destination_directory}")
    else:
        print(f"文件 {file_to_move} 不存在，无法移动。")
except Exception as e:
    print(f"移动 printAndLog.py 文件失败: {e}")
    print("请手动移动到 script/tools 目录下，同时 printAndLog.py 可能不在根目录下！")
    input("初始化失败！")
    sys.exit()

# 添加script目录到sys.path
sys.path.append(os.path.join('script'))

from script import addBackMovie
from script import addEmptyJson
from script import addNewConfigFile
from script.tools import printAndLog

log_file_path = os.path.join("logs/")
formatted_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
log_file_name = f"初始化日志_{formatted_time}.log"

# 将 ffmpeg 路径添加到环境变量
path_ffmpeg_to_add = os.path.join(application_path, "script", "ffmpeg", "bin")
try:
    printAndLog.log_and_print("正在添加 ffmpeg 文件夹到路径", log_file_path, log_file_name)
    subprocess.run(['setx', 'PATH', f'%PATH%;{path_ffmpeg_to_add}'], check=True)
    printAndLog.log_and_print(f"已将 {path_ffmpeg_to_add} 永久添加到系统PATH环境变量中", log_file_path, log_file_name)
except subprocess.CalledProcessError as e:
    printAndLog.log_and_print(f"添加 {path_ffmpeg_to_add} 到系统PATH环境变量失败: {e}", log_file_path, log_file_name)
    printAndLog.log_and_print(f"请手动添加{path_ffmpeg_to_add}路径到环境变量", log_file_path, log_file_name)
    input()
# 初始化 config 文件
printAndLog.log_and_print("\n<---------- 初始化配置 ---------->", log_file_path, log_file_name)
config_file_path = os.path.join("configs/config.yaml")
addNewConfigFile.creat_new_config_file(config_file_path)
addNewConfigFile.add_game_path(config_file_path)
printAndLog.log_and_print("\n<---------- 初始化临时文件 ---------->", log_file_path, log_file_name)
# 初始化视频
output_file_name = os.path.join("output_video.mp4")
ffmpeg_path = os.path.join("script/ffmpeg/bin/ffmpeg.exe")
cmd_log_level = os.path.join("debug")
work_path = os.path.join("script/temp/")
addBackMovie.add_empty_video(output_file_name, ffmpeg_path, cmd_log_level, work_path, 'logs/', f"初始化日志_{formatted_time}.log")
# 初始化 json 文件
json_output_filename = 'script/temp/output.json'
addEmptyJson.add_empty_json_file(json_output_filename)

printAndLog.log_and_print("\n初始化已完成！按任意键继续...", log_file_path, log_file_name)
input("")
