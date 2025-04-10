import os
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip

def merge_single_video(a_path, b_video_path, output_path):
    # 加载A视频并设置分辨率
    clip_a = VideoFileClip(a_path).resize((720, 1280))

    # 创建纯黑色区域（720x540）
    black_box = ColorClip(size=(720, 540), color=(0, 0, 0), duration=clip_a.duration)
    black_box = black_box.set_position(("center", "center"))

    # 加载B视频，宽度设为710，高度等比缩放
    clip_b = VideoFileClip(b_video_path)
    new_width = 710
    aspect_ratio = clip_b.h / clip_b.w
    new_height = int(new_width * aspect_ratio)
    clip_b_resized = clip_b.resize((new_width, new_height)).set_position(("center", "center"))
    clip_b_resized = clip_b_resized.set_duration(clip_a.duration)

    # 合成视频
    final = CompositeVideoClip([clip_a, black_box, clip_b_resized])

    # 导出视频
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")


def batch_merge_videos(a_path, b_folder_path, output_folder_path):
    # 确保输出目录存在
    os.makedirs(output_folder_path, exist_ok=True)

    # 遍历B视频文件夹
    for filename in os.listdir(b_folder_path):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            b_video_path = os.path.join(b_folder_path, filename)
            output_path = os.path.join(output_folder_path, filename)
            print(f"处理视频: {filename}")
            merge_single_video(a_path, b_video_path, output_path)
            print(f"保存至: {output_path}\n")


# 示例调用
batch_merge_videos(
    a_path="rotated_video.mp4",
    b_folder_path="./Videos",
    output_folder_path="./MergeVideos"
)
