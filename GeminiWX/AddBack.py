from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.fx.resize import resize

def align_video_a_to_b(video_a_path, video_b_path, output_path):
    # 加载视频
    clip_a = VideoFileClip(video_a_path)
    clip_b = VideoFileClip(video_b_path)

    duration_a = clip_a.duration
    duration_b = clip_b.duration

    if duration_a > duration_b:
        # A 比 B 长，剪切 A
        new_clip_a = clip_a.subclip(0, duration_b)
    else:
        # A 比 B 短，重复 A 直到和 B 一样长
        clips = []
        total_duration = 0
        while total_duration < duration_b:
            remaining = duration_b - total_duration
            if remaining < duration_a:
                clips.append(clip_a.subclip(0, remaining))
                total_duration += remaining
            else:
                clips.append(clip_a)
                total_duration += duration_a
        new_clip_a = concatenate_videoclips(clips)

    # 保存结果
    new_clip_a.write_videofile(output_path, codec="libx264")

    # 清理资源
    clip_a.close()
    clip_b.close()
    new_clip_a.close()




def embed_b_in_a(video_a_path, video_b_path, output_path):
    # 加载视频
    # clip_a = VideoFileClip(video_a_path, audio=False)
    # clip_b = VideoFileClip(video_b_path, audio=False)
    clip_a = VideoFileClip(video_a_path , audio=False)
    clip_b = VideoFileClip(video_b_path , audio=False)

    # 获取 B 的尺寸
    b_w, b_h = clip_b.size

    # 计算新的 A 视频尺寸
    new_a_w = b_w
    new_a_h = b_h + 200  # 上下各100像素

    # 调整 A 的分辨率
    clip_a_resized = resize(clip_a, height=new_a_h, width=new_a_w)

    # 把 B 放在 A 中间（居中）
    b_position = ('center', 'center')

    # 合成视频
    final = CompositeVideoClip([
        clip_a_resized,
        clip_b.set_position(b_position)
    ], size=(new_a_w, new_a_h))

    # 设置导出参数（保持音频，设置帧率）
    final.set_duration(min(clip_a.duration, clip_b.duration)) \
         .write_videofile(output_path, codec="libx264", audio_codec="aac")

# 示例用法
# embed_b_in_a("video_a.mp4", "video_b.mp4", "output.mp4")


def align_video_a_to_b2(video_a_path, video_b_path, output_path):
    # 加载视频
    clip_a = VideoFileClip(video_a_path)
    clip_b = VideoFileClip(video_b_path)

    duration_a = clip_a.duration
    duration_b = clip_b.duration

    if duration_a > duration_b:
        # A 比 B 长，剪切 A
        new_clip_a = clip_a.subclip(0, duration_b)
    else:
        # A 比 B 短，重复 A 直到和 B 一样长
        clips = []
        total_duration = 0
        while total_duration < duration_b:
            remaining = duration_b - total_duration
            if remaining < duration_a:
                clips.append(clip_a.subclip(0, remaining))
                total_duration += remaining
            else:
                clips.append(clip_a)
                total_duration += duration_a
        new_clip_a = concatenate_videoclips(clips)

    # 保留音频
    new_clip_a.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # 清理资源
    clip_a.close()
    clip_b.close()
    new_clip_a.close()

# 示例调用
# align_video_a_to_b("video_a.mp4", "video_b.mp4", "video_a_aligned.mp4")
align_video_a_to_b2("D:\\Gemini\\BackVideo\\back.mp4", "D:\\Gemini\\OutV\\1_merged.mp4","result2.mp4" )
embed_b_in_a("result2.mp4", "D:\\Gemini\\OutV\\1_merged.mp4", "result3.mp4")

