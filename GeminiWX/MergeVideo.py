from moviepy.editor import VideoFileClip, AudioFileClip

# def merge_video_audio(video_path, audio_path, output_path):
#     """
#     将 MP4 视频和 WAV 音频合成一个新视频。
#
#     :param video_path: 输入视频文件路径 (MP4)
#     :param audio_path: 输入音频文件路径 (WAV)
#     :param output_path: 输出合成后的视频文件路径 (MP4)
#     """
#     # 加载视频
#     video = VideoFileClip(video_path)
#
#     # 加载音频
#     audio = AudioFileClip(audio_path)
#
#     # 调整音频长度，使其与视频匹配
#     audio = audio.subclip(0, min(video.duration, audio.duration))
#
#     # 将音频添加到视频
#     final_video = video.set_audio(audio)
#
#     # 导出合成后的视频
#     final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
#
# # 示例调用
# merge_video_audio("./OutV/1.mp4", "example.wav", "output.mp4")


import os
from moviepy.editor import VideoFileClip, AudioFileClip


# def merge_video_audio_files(video_dir, audio_dir, output_dir):
#     """
#     遍历 video_dir 和 audio_dir，将具有相同前缀的 MP4 视频和 WAV 音频合成新视频，并保存到 output_dir。
#
#     :param video_dir: 存放视频文件的目录
#     :param audio_dir: 存放音频文件的目录
#     :param output_dir: 输出合成后视频的目录
#     """
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#
#     video_files = {os.path.splitext(f)[0]: os.path.join(video_dir, f) for f in os.listdir(video_dir) if
#                    f.endswith(".mp4")}
#     audio_files = {os.path.splitext(f)[0]: os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if
#                    f.endswith(".wav")}
#
#     common_prefixes = set(video_files.keys()) & set(audio_files.keys())
#
#     for prefix in common_prefixes:
#         video_path = video_files[prefix]
#         audio_path = audio_files[prefix]
#         output_path = os.path.join(output_dir, f"{prefix}_merged.mp4")
#
#         print(f"正在合并: {video_path} + {audio_path} -> {output_path}")
#         try:
#             video = VideoFileClip(video_path)
#             audio = AudioFileClip(audio_path)
#             audio = audio.subclip(0, min(video.duration, audio.duration))
#             final_video = video.set_audio(audio)
#             final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
#         except Exception as e:
#             print(f"合并 {prefix} 失败: {e}")
#
#
# # 示例调用
# merge_video_audio_files("./Videos", "./output_wavs", "./OutV")


# import os
# from moviepy.editor import VideoFileClip, AudioFileClip
#
#
# def merge_video_audio_files(video_dir, audio_dir, output_dir):
#     """
#     遍历 video_dir 和 audio_dir，将具有相同前缀的 MP4 视频和 WAV 音频合成新视频，并保存到 output_dir。
#
#     :param video_dir: 存放视频文件的目录
#     :param audio_dir: 存放音频文件的目录
#     :param output_dir: 输出合成后视频的目录
#     """
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#
#     video_files = {os.path.splitext(f)[0]: os.path.join(video_dir, f) for f in os.listdir(video_dir) if
#                    f.endswith(".mp4")}
#     audio_files = {os.path.splitext(f)[0]: os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if
#                    f.endswith(".wav")}
#
#     common_prefixes = set(video_files.keys()) & set(audio_files.keys())
#
#     for prefix in common_prefixes:
#         video_path = video_files[prefix]
#         audio_path = audio_files[prefix]
#         output_path = os.path.join(output_dir, f"{prefix}_merged.mp4")
#
#         print(f"正在合并: {video_path} + {audio_path} -> {output_path}")
#         try:
#             video = VideoFileClip(video_path).subclip(0, min(AudioFileClip(audio_path).duration, VideoFileClip(video_path).duration))
#             audio = AudioFileClip(audio_path).subclip(0, min(AudioFileClip(audio_path).duration, AudioFileClip(audio_path).duration))
#
#             final_video = video.set_audio(audio)
#             final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
#         except Exception as e:
#             print(f"合并 {prefix} 失败: {e}")
#
#
# # 示例调用
# merge_video_audio_files("./Videos", "./output_wavs", "./OutV")


import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips


def merge_video_audio_files(video_dir, audio_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_files = {os.path.splitext(f)[0]: os.path.join(video_dir, f) for f in os.listdir(video_dir) if
                   f.endswith(".mp4")}
    audio_files = {os.path.splitext(f)[0]: os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if
                   f.endswith(".wav")}

    common_prefixes = set(video_files.keys()) & set(audio_files.keys())

    for prefix in common_prefixes:
        video_path = video_files[prefix]
        audio_path = audio_files[prefix]
        output_path = os.path.join(output_dir, f"{prefix}_merged.mp4")
        final_output_path = os.path.join(output_dir, f"{prefix}_final.mp4")

        try:
            original_video = VideoFileClip(video_path)
            video_duration = original_video.duration
            audio_duration = AudioFileClip(audio_path).duration

            min_duration = min(video_duration, audio_duration)
            final_video = original_video.subclip(0, min_duration).set_audio(
                AudioFileClip(audio_path).subclip(0, min_duration))

            # 替换原始视频的对应时长部分
            final_video2 = concatenate_videoclips([final_video])
            final_video2 = final_video2.subclip(0, min(15, final_video2.duration))  # 截取前15秒

            final_video2.write_videofile(final_output_path, codec="libx264", audio_codec="aac")
            print(f"成功生成: {final_output_path}")
        except Exception as e:
            print(f"合并 {prefix} 失败: {e}")


# 示例调用
merge_video_audio_files("./Videos", "./output_wavs", "./OutV")
