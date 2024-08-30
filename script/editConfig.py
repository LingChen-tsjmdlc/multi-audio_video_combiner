import re
import sys

import yaml

sys.path.append('./script')  # 添加script目录到sys.path
from script.tools import printAndLog

def edit_config(config_path, log_file_path, log_file_name):
    # 读取用户输入的路径，并确保不为空
    while True:
        printAndLog.log_and_print("1.输入渲染完成后序列帧路径：", log_file_path, log_file_name)
        render_dir = input("")
        if render_dir:
            render_dir = render_dir.replace('\\', '/')
            printAndLog.log_and_print(f"---> 当前渲染路径输入：{render_dir}", log_file_path, log_file_name, True)
            break
        else:
            printAndLog.log_and_print("-X- 路径不能为空，请重新输入。", log_file_path, log_file_name)

    # 读取用户输入的帧数，并确保不为空且在0到240之间
    while True:
        printAndLog.log_and_print("2.输入导出视频所需要的帧数【必须是整数！】：", log_file_path, log_file_name)
        farm_output = input("")
        if farm_output.isdigit() and 0 < int(farm_output) < 240:
            farm_output = int(farm_output)
            printAndLog.log_and_print(f"---> 当前导出视频帧数设置：{farm_output} fps/s", log_file_path, log_file_name,
                                      True)
            break
        else:
            printAndLog.log_and_print("-X- 帧数必须是一个大于0且小于240的整数，请重新输入。", log_file_path,
                                      log_file_name)

    # 获取音频的路径
    while True:
        printAndLog.log_and_print("3.输入音频的路径(不填写表示使用默认)：", log_file_path, log_file_name)
        audio_dir = input("")
        if audio_dir:
            audio_dir = audio_dir.replace('\\', '/')
            printAndLog.log_and_print(f"---> 当前输入音频的路径：{audio_dir}", log_file_path, log_file_name)
            break
        else:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            default_dir = config['game_dir']
            printAndLog.log_and_print(
                f"---> 已经使用默认音频路径:{default_dir}/ResourceForPlayer/userdata/external_sound", log_file_path,
                log_file_name, True)
            print(f"已经使用默认音频路径:{default_dir}/ResourceForPlayer/userdata/external_sound")
            default_audio_dir = f"{default_dir}/ResourceForPlayer/userdata/external_sound"
            config['default_audio_dir'] = default_audio_dir
            config['audio_dir'] = None
            with open(config_path, 'w', encoding='utf-8') as file:
                yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
            break

    while True:
        printAndLog.log_and_print("4.输入movie文件的路径：", log_file_path, log_file_name)
        movie_file_save_dir = input("")
        if movie_file_save_dir:
            printAndLog.log_and_print("5.输入movie文件的文件名：", log_file_path, log_file_name)
            movie_file_name = input("")
            if movie_file_name:
                movie_save_dir = f"{movie_file_save_dir}/{movie_file_name}.movie"
                movie_save_dir = movie_save_dir.replace('\\', '/')
                printAndLog.log_and_print(f"---> 当前输入的工程文件路径：{movie_save_dir}", log_file_path, log_file_name,
                                          True)
                break  # 一旦两个输入都不为空，退出循环
            else:
                printAndLog.log_and_print("-X- 文件名不能为空，请重新输入。", log_file_path, log_file_name)
        else:
            printAndLog.log_and_print("-X- 路径不能为空，请重新输入。", log_file_path, log_file_name)

    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    # 更新配置
    config['render_dir'] = render_dir
    config['farm_output'] = farm_output
    config['audio_dir'] = audio_dir
    config['movie_save_dir'] = movie_save_dir

    # 将更新后的数据写回YAML文件
    with open(config_path, 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False, allow_unicode=True)

    printAndLog.log_and_print("配置已更新。", log_file_path, log_file_name)
    printAndLog.log_and_print(f"当前配置：{config}\n\n\n", log_file_path, log_file_name,True)


if __name__ == "__main__":
    config_path = "../configs/config.yaml"
    log_file_dir = '../logs/'
    log_name = '配置文件日志'
    edit_config(config_path, log_file_dir, log_name)
