from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.fx import all as fx
import os

def merge_video_audio_files_fast(video_dir, audio_dir, output_dir, target_duration=12):
    """
    遍历 video_dir 和 audio_dir，将具有相同前缀的 MP4 视频和 WAV 音频合成新视频，并保存到 output_dir。
    视频和音频将被调整速率，使视频的最终播放时间为 target_duration 秒。

    :param video_dir: 存放视频文件的目录
    :param audio_dir: 存放音频文件的目录
    :param output_dir: 输出合成后视频的目录
    :param target_duration: 最终视频的目标时长，默认为 10 秒
    """
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

        print(f"正在合并: {video_path} + {audio_path} -> {output_path}")
        try:
            # 获取视频和音频的时长
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)

            # 动态计算提速倍数
            speed_factor = video_clip.duration / target_duration

            # 提速视频和音频
            video_clip = fx.speedx(video_clip, speed_factor)
            # audio_clip = audio_clip.set_fps(audio_clip.fps * speed_factor)
            # audio_clip = audio_clip.set_fps(audio_clip.fps)

            # 截取音视频时长一致
            video_clip = video_clip.subclip(0, min(audio_clip.duration, video_clip.duration))
            audio_clip = audio_clip.subclip(0, video_clip.duration)

            final_video = video_clip.set_audio(audio_clip)
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
        except Exception as e:
            print(f"合并 {prefix} 失败: {e}")

merge_video_audio_files_fast("./Videos", "./output_wavs", "./OutV")