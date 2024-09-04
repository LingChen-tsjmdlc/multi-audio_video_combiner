# 多音频 视频 混合器（大宋映画特制版）
主要解决用户使用 [大宋映画](https://n.163.com/2021/dsyhjs/) 时,导出视频还要对轨音频的问题，同时还提供自动字幕功能。
> **大宋映画**：大宋映画是一款基于《逆水寒》游戏的动画编辑器，它允许用户零基础快速上手，成为古装大片的“导演”。
> 这款软件具备强大的功能，如角色外观的自由组合与创造、骨骼参数调节、细致的表情控制，甚至AI表情捕捉，
> 以及场景和天气的自由调节。用户可以创建独特的角色、制作动作和表情，以及搭建各种场景，实现电影级的动画制作。
---


## 目录：
* [功能](#功能)
* [使用指南](#食用指北-使用指南)
  * [整合包](#使用整合包推荐)
  * [源代码](#使用源代码)
* [开发上手指南](#开发上手指南)
  * [环境要求](#环境要求)
  * [程序要求](#程序要求)
* [项目结构](#项目结构)
  * [结构及说明](#结构及说明)
  * [功能模块说明](#功能模块说明)



## 功能：
1. [x] 自动合并序列帧
2. [x] 对轨音频
3. [ ] 根据音频时间轴上字幕



## ~~食用指北~~  使用指南：

### 使用整合包【_推荐_】
1. 在 [releases](https://github.com/LingChen-tsjmdlc/multi-audio_video_combiner/releases) 处下载整合包
2. 按照以下顺序运行:
   1. 初始化【只在最开始的时候运行一次！】
   2. 配置修改
3. 在 [Output](Output) 文件夹下查看输出结果，文件名称是 output_file.mp4

### 使用源代码
1. 阅读 [程序要求](#程序要求) 来安装所有相关内容
2. 按照以下顺序运行:
   1. 运行 addBackMovie.py 初始化一个空视频
   2. 运行 addEmptyJson.py 初始化一个 json 文件
   3. 运行 change_config.py 来修改配置，当然你也可以在 [config.yaml](configs/config.yaml) 中直接修改
   4. 运行 main.py
3. 在 [Output](Output) 文件夹下查看输出结果，文件名称是 output_file.mp4



## 开发上手指南：

### 环境要求
1. 系统要求：支持 Windows 系统（项目使用 python，理论上 mac 和 linux 皆可使用，如需使用请自行编译）
2. 软件要求：必须安装大宋映画及相关内容，需要 ffmpeg 环境（整合包已自带）
3. 网络状况：无需联网即可使用

### 程序要求
1. 推荐使用 PyCharm 作为 IDE，**使用 Python 3.9 版本**
2. 【**_如果有ffmpeg且已经配置好环境变量则跳过 2~4 步_**】下载 [ffmpeg](https://ffmpeg.org/download.html)
3. 将下载好的 ffmpeg 解压，将 bin 文件夹中的 ffmpeg.exe 和 ffprobe.exe 复制到 [script/ffmpeg/bin](script/ffmpeg/bin)
4. 将 [script/ffmpeg/bin](script/ffmpeg/bin) 添加到环境变量
5. 安装 requirements.txt 的所有依赖



## 项目结构：

### 结构及说明
- **build**: 存放构建脚本或编译输出文件。
- **configs**: 配置文件目录，包括主配置文件 [config.yaml](configs/config.yaml)。
- **dist**: 打包分发文件夹。
- **logs**: 日志文件存放区，分为不同类型的日志子目录。
- **Output**: 输出结果存放区。
- **script**: 脚本文件目录
    - ffmpeg: 与 ffmpeg 相关的脚本或配置文件。
      - bin: ffmpeg 的可执行程序
      - license.txt
      - readme.md
    - script: 其他脚本文件。
    - temp: 临时文件存放区。
    - tools: 工具脚本或可执行文件存放区。
- **Test**: 测试相关文件或测试脚本存放区。
- **_initialization_**:初始化项目（打包后使用的）
- **_change_config_**:修改配置文件的主程序
- **_main_**:主程序（自动合并序列帧和对轨音频）
- **.gitignore**: Git 忽略文件列表。
- **requirements.txt**: Python 环境依赖项清单。
- **README.md**: 项目说明文档
- 
### 功能模块说明
- addBackMovie.py: 初始化视频文件，功能是生成一个 1s 的空视频。
- addEmptyJson.py: 初始化JSON文件。
- addNewConfigFile.py: 初始化配置文件。
- AudioMix.py: 音频混合处理脚本。
- editConfig.py: 编辑配置文件的工具。
- getAudioStartTimeAndName.py: 获取音频开始时间和名称。
- getVideoTime.py: 获取视频时长信息。
- Mixer.py: 视频与音频混音器脚本。
- VideoMix.py: 序列帧合成视频处理脚本。

## 开源协议
**该项目签署了 [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) 授权许可，详情请参阅 LICENSE.txt**