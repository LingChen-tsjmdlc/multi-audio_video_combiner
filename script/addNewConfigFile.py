import os
import time
import logging
import yaml

# 设置日志文件名
base_log_filename = '初始化日志'
log_filename = f"{base_log_filename}_{time.strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_directory = 'logs'
log_filepath = os.path.join(log_directory, log_filename)
# 确保日志目录存在
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
# 配置日志记录器
logging.basicConfig(
    filename=log_filepath,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# 创建日志记录器
logger = logging.getLogger()


def log_and_print(message):
    print(message)
    logger.info(message)


# 定义config.yaml文件中的键值对
config_data = {
    "audio_dir": "",
    "def_farm": 28,
    "default_audio_dir": "",
    "farm_output": 0,
    "game_dir": "",
    "movie_save_dir": "",
    "render_dir": "",
    "video_time": 0
}


def creat_new_config_file(config_file_path):
    # 生成config.yaml文件内容
    config_yaml = yaml.dump(config_data, allow_unicode=True, sort_keys=False)

    # 创建config.yaml文件
    with open(config_file_path, 'w', encoding='utf-8') as file:
        file.write(config_yaml)

    log_and_print('config.yaml文件已生成。')


def add_game_path(config_file_path):
    with open(config_file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    log_and_print("\n------《逆水寒》游戏的 res 路径------")
    log_and_print("例如 F:/LiShuiHan/逆水寒/artist/res ")
    log_and_print("这个路径一般在你安装游戏的目录下 的 ”artist“ 目录下的 ”res“ ")
    while True:
        game_path = input("请输入你游戏的res路径：")
        if game_path.strip():
            game_path = game_path.replace('\\', '/')
            log_and_print(f"你输入的路径是{game_path}")
            break
        else:
            log_and_print("输入不能为空，请重新输入。")

    config['game_dir'] = game_path
    config['default_audio_dir'] = f"{game_path}/ResourceForPlayer/userdata/external_sound"

    # 将更新后的配置写回文件
    with open(config_file_path, 'w', encoding='utf-8') as file:
        yaml.dump(config, file, allow_unicode=True, sort_keys=False)


if __name__ == "__main__":
    try:
        config_file_path = "../configs/config.yaml"
        creat_new_config_file(config_file_path)
        add_game_path(config_file_path)
    finally:
        # 无论程序是否正常结束，都关闭日志文件
        logging.shutdown()
