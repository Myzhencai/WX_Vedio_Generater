from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip


def merge_videos(a_path, b_path, output_path="output.mp4"):
    # 加载A视频
    clip_a = VideoFileClip(a_path).resize((720, 1280))

    # 创建纯黑色区域（720x540）
    black_box = ColorClip(size=(720, 540), color=(0, 0, 0), duration=clip_a.duration)
    black_box = black_box.set_position(("center", "center"))

    # 加载B视频，宽度设为710，高度等比缩放
    clip_b = VideoFileClip(b_path)
    new_width = 710
    aspect_ratio = clip_b.h / clip_b.w
    new_height = int(new_width * aspect_ratio)
    clip_b_resized = clip_b.resize((new_width, new_height)).set_position(("center", "center"))

    # 截断B视频到和A视频一样长（以防超出）
    clip_b_resized = clip_b_resized.set_duration(clip_a.duration)

    # 合成视频（A视频+黑框+B视频）
    final = CompositeVideoClip([clip_a, black_box, clip_b_resized])

    # 导出
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

merge_videos("rotated_video.mp4", "./Videos/1.mp4", "merged_output.mp4")
