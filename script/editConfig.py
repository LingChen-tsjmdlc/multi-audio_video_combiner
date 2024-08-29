import os
import shutil
import yaml


def edit_config():
    # 读取用户输入的路径，并确保不为空
    while True:
        render_dir = input("输入渲染完成后序列帧路径：")
        if render_dir:
            render_dir = render_dir.replace('\\', '/')
            break
        else:
            print("路径不能为空，请重新输入。\n")

    # 读取用户输入的帧数，并确保不为空且在0到240之间
    while True:
        farm_output = input("输入导出视频所需要的帧数【必须是整数！】：")
        if farm_output.isdigit() and 0 < int(farm_output) < 240:
            farm_output = int(farm_output)
            break
        else:
            print("帧数必须是一个大于0且小于240的整数，请重新输入。\n")

    # 获取音频的路径
    while True:
        audio_dir = input("输入音频的路径(不填写表示使用默认)：")
        if audio_dir:
            audio_dir = audio_dir.replace('\\', '/')
            break
        else:
            with open('configs/config_temp.yaml', 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            default_dir = config['game_dir']
            print(f"已经使用默认路径:{default_dir}/ResourceForPlayer/userdata/external_sound")
            default_audio_dir = f"{default_dir}/ResourceForPlayer/userdata/external_sound"
            config['default_audio_dir'] = default_audio_dir
            config['audio_dir'] = None
            with open('configs/config_temp.yaml', 'w', encoding='utf-8') as file:
                yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
            break

    while True:
        movie_file_save_dir = input("输入movie文件的路径：")
        if movie_file_save_dir:
            movie_file_name = input("输入movie文件的文件名：")
            if movie_file_name:
                movie_save_dir = f"{movie_file_save_dir}/{movie_file_name}.movie"
                movie_save_dir = movie_save_dir.replace('\\', '/')
                break  # 一旦两个输入都不为空，退出循环
            else:
                print("文件名不能为空，请重新输入。")
        else:
            print("路径不能为空，请重新输入。")

    with open('configs/config_temp.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    # 更新配置
    config['render_dir'] = render_dir
    config['farm_output'] = farm_output
    config['audio_dir'] = audio_dir
    config['movie_save_dir'] = movie_save_dir

    # 将更新后的数据写回YAML文件
    with open('configs/config_temp.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False, allow_unicode=True)

    print("配置已更新。")
    if os.path.exists('configs/config.yaml'):
        os.remove('configs/config.yaml')
    shutil.copy('configs/config_temp.yaml', 'configs/config.yaml')
    print(f"{config}")


if __name__ == "__main__":
    edit_config()