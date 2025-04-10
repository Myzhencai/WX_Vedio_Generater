from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
import os
#
# def adjust_and_embed_video(video_a_path, video_b_path, output_path='output.mp4'):
#     # 加载视频
#     clip_a = VideoFileClip(video_a_path)
#     clip_b = VideoFileClip(video_b_path)
#
#     # Step 1: 调整 A 的时长以匹配 B 的时长
#     if clip_b.duration < clip_a.duration:
#         clip_a = clip_a.subclip(0, clip_b.duration)
#     else:
#         clips = []
#         duration_needed = clip_b.duration
#         while sum(c.duration for c in clips) < duration_needed:
#             clips.append(clip_a)
#         clip_a = concatenate_videoclips(clips).subclip(0, clip_b.duration)
#
#     # Step 2: 将 A 缩放并嵌入到 B 中，保持 A 的原始分辨率比例
#     target_width = clip_b.w
#     target_height = clip_b.h
#
#     # 计算嵌入区域的最大高度和宽度
#     embed_height = target_height - 500  # 上下各留 80px
#     scale_factor = min(1, embed_height / clip_a.h)
#     resized_a = clip_a.resize(height=int(clip_a.h * scale_factor))
#
#     # 计算嵌入位置（居中）
#     a_x = (target_width - resized_a.w) // 2
#     a_y = 250
#
#     # 合成视频
#     final = CompositeVideoClip([
#         clip_b,
#         resized_a.set_position((a_x, a_y))
#     ])
#
#     final.set_duration(clip_b.duration).write_videofile(output_path, codec="libx264")
#
#     # 释放资源
#     clip_a.close()
#     clip_b.close()
#     final.close()


from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip

def process_videos(video_a_path, video_b_path, output_path):
    # 加载视频
    video_a = VideoFileClip(video_a_path).without_audio()
    video_b = VideoFileClip(video_b_path)

    # Step 1: 调整A的时长以匹配B
    if video_a.duration > video_b.duration:
        video_a = video_a.subclip(0, video_b.duration)
    else:
        # 重复A直到时长 >= B，然后再裁剪精确一致
        clips = []
        duration_accum = 0
        while duration_accum < video_b.duration:
            clips.append(video_a)
            duration_accum += video_a.duration
        video_a = concatenate_videoclips(clips).subclip(0, video_b.duration)

    # Step 2: 调整A的分辨率（宽度 = B宽度，A高度 = B高度 + 200）
    target_width = video_b.w
    target_height = video_b.h + 200
    video_a_resized = video_a.resize((target_width, target_height))

    # Step 3: 将B嵌入A中（居中、右对齐、上下差100像素）
    b_position = ("center", 100)  # x居中，y从上边100像素开始
    composite = CompositeVideoClip([video_a_resized, video_b.set_position(b_position)])
    composite = composite.set_duration(video_b.duration)

    # Step 4: 设置B的视频音频为输出音频
    composite = composite.set_audio(video_b.audio)

    # 导出合成视频
    composite.write_videofile(output_path, codec='libx264', audio_codec='aac')


# 示例调用
process_videos("D:\\Gemini\\BackVideo\\back.mp4", "D:\\Gemini\\OutV\\1_merged.mp4", "result.mp4")
