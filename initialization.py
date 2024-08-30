import sys
import os
import time

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
        if not os.path.exists(ffmpeg_destination_path):
            os.rename(ffmpeg_source_path, ffmpeg_destination_path)
            print(f"ffmpeg.exe 已移动到 {ffmpeg_destination_path}")
        else:
            print(f"{ffmpeg_destination_path} 已存在，未移动 ffmpeg.exe")
    except Exception as e:
        print(f"移动 ffmpeg.exe 失败: {e}")
        input("初始化失败！")
        sys.exit()
else:
    print("ffmpeg.exe 不在根目录下")
    input("初始化失败！")
    sys.exit()

# 移动 printAndLog.py
file_to_move = os.path.join("printAndLog.py")   # 定义要移动的文件路径
destination_directory = os.path.join("script/tools")    # 定义目标目录路径
if not os.path.exists(destination_directory):   # 检查目标目录是否存在，如果不存在则创建
    os.makedirs(destination_directory)
try:    # 尝试移动文件
    if os.path.exists(file_to_move):
        os.rename(file_to_move, os.path.join(destination_directory, os.path.basename(file_to_move)))
        print(f"文件已成功移动到 {destination_directory}")
    else:
        print(f"文件 {file_to_move} 不存在，无法移动。")
except Exception as e:
    print(f"移动文件失败: {e}")
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
