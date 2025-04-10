from moviepy.editor import VideoFileClip, concatenate_videoclips


def replace_video_segment(video1_path, video2_path, start_time, output_path):
    """
    用 video1 替换 video2 中从 start_time 开始、时长相同的部分，并合成新视频。

    :param video1_path: str, video1 文件路径
    :param video2_path: str, video2 文件路径
    :param start_time: float, video1 替换 video2 的开始时间（秒）
    :param output_path: str, 输出合成视频的路径
    """

    # 读取视频文件
    video1 = VideoFileClip(video1_path)
    video2 = VideoFileClip(video2_path)

    # 计算 video1 结束时间
    end_time = start_time + video1.duration

    # 截取 video2 的片段（开始部分 + 结束部分）
    before = video1.subclip(0, end_time)
    after = video2.subclip(end_time, end_time+6)

    # 合成新视频
    final_video = concatenate_videoclips([before, after])

    # 输出最终视频
    final_video.write_videofile(output_path, codec='libx264', fps=video2.fps)

    # 释放资源
    video1.close()
    video2.close()
    final_video.close()

# 示例用法
replace_video_segment("D:\\Gemini\\OutV\\1_merged.mp4", "D:\\Gemini\\Videos\\1.mp4", 0, "D:\\Gemini\\Videos\\output.mp4")