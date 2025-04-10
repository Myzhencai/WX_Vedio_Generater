from moviepy.editor import AudioFileClip, TextClip, CompositeVideoClip
from moviepy.editor import VideoFileClip
# 加载原始视频
video = VideoFileClip("your_video.mp4")

# 加载生成的语音
audio = AudioFileClip("output_audio.mp3")

# 设置视频的音频为生成的语音
video = video.set_audio(audio)

# 创建字幕
subtitle = TextClip(text, fontsize=24, color='white', bg_color='black', size=video.size)
subtitle = subtitle.set_position('bottom').set_duration(video.duration)

# 合成视频
final_video = CompositeVideoClip([video, subtitle])

# 输出最终视频
final_video.write_videofile("output_video.mp4", codec='libx264')
