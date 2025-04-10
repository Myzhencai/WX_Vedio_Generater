import os
from moviepy.editor import VideoFileClip


def trim_videos(input_folder: str, output_folder: str, duration: int = 10):
    """
    读取 input_folder 目录下的所有 MP4 文件，将它们剪辑为 duration 秒的短视频，
    并将结果保存到 output_folder。

    :param input_folder: 原始视频文件夹
    :param output_folder: 剪辑后的视频文件夹
    :param duration: 剪辑的时长（秒），默认为 10 秒
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".mp4"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                with VideoFileClip(input_path) as video:
                    trimmed = video.subclip(0, min(duration, video.duration))
                    trimmed.write_videofile(output_path, codec='libx264', fps=video.fps)
                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# 使用示例
trim_videos("Videos", "OutV")
