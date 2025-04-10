import os
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip, concatenate_videoclips

# def merge_single_video(a_path, b_video_path, output_path):
#     # 加载B视频
#     clip_b = VideoFileClip(b_video_path)
#     b_duration = clip_b.duration
#
#     # 加载A视频并设置分辨率
#     clip_a = VideoFileClip(a_path).resize((720, 1280))
#
#     # 调整A视频时长：循环或裁剪以匹配B
#     if clip_a.duration < b_duration:
#         n_loops = int(b_duration // clip_a.duration) + 1
#         clip_a = concatenate_videoclips([clip_a] * n_loops).subclip(0, b_duration)
#     else:
#         clip_a = clip_a.subclip(0, b_duration)
#
#     # 创建黑色区域（720x480）遮罩，时长也匹配B
#     black_box = ColorClip(size=(720, 480), color=(0, 0, 0), duration=b_duration)
#     black_box = black_box.set_position(("center", "center"))
#
#     # 缩放并设置B视频位置
#     new_width = 710
#     aspect_ratio = clip_b.h / clip_b.w
#     new_height = int(new_width * aspect_ratio)
#     clip_b_resized = clip_b.resize((new_width, new_height)).set_position(("center", "center"))
#
#     # 合成最终视频
#     final = CompositeVideoClip([clip_a, black_box, clip_b_resized], size=(720, 1280))
#     final = final.set_duration(b_duration)
#
#     # 判断音频是否可用
#     has_audio = clip_a.audio is not None and clip_b.audio is not None
#
#     # 输出
#     final.write_videofile(
#         output_path,
#         codec="libx264",
#         audio_codec="aac" if has_audio else None,
#         audio=has_audio
#     )

def merge_single_video(a_path, b_video_path, output_path):
    with VideoFileClip(b_video_path) as clip_b, VideoFileClip(a_path).resize((720, 1280)) as clip_a:
        b_duration = clip_b.duration

        if clip_a.duration < b_duration:
            n_loops = int(b_duration // clip_a.duration) + 1
            clip_a = concatenate_videoclips([clip_a] * n_loops).subclip(0, b_duration)
        else:
            clip_a = clip_a.subclip(0, b_duration)

        black_box = ColorClip(size=(720, 480), color=(0, 0, 0), duration=b_duration)
        black_box = black_box.set_position(("center", "center"))

        new_width = 710
        aspect_ratio = clip_b.h / clip_b.w
        new_height = int(new_width * aspect_ratio)
        clip_b_resized = clip_b.resize((new_width, new_height)).set_position(("center", "center"))

        final = CompositeVideoClip([clip_a, black_box, clip_b_resized], size=(720, 1280)).set_duration(b_duration)

        has_audio = clip_a.audio is not None and clip_b.audio is not None

        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac" if has_audio else None,
            audio=has_audio
        )

        final.close()



def batch_merge_videos(a_path, b_folder_path, output_folder_path):
    os.makedirs(output_folder_path, exist_ok=True)

    for filename in os.listdir(b_folder_path):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            b_video_path = os.path.join(b_folder_path, filename)
            output_path = os.path.join(output_folder_path, filename)
            print(f"处理视频: {filename}")
            try:
                merge_single_video(a_path, b_video_path, output_path)
            except Exception as e:
                print(f"⚠️ 处理 {filename} 时出错: {e}")
            print()

# 示例调用
batch_merge_videos(
    a_path="rotated_video.mp4",
    b_folder_path="./Videos",
    output_folder_path="./MergedOutputs"
)
