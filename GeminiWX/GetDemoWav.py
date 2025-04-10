from moviepy.editor import VideoFileClip

from moviepy.editor import VideoFileClip

def extract_audio_wav(input_video: str, output_audio: str):
    """
    从 MP4 视频中提取前 30 秒的音频并保存为 WAV 格式。

    :param input_video: 输入 MP4 文件路径
    :param output_audio: 输出 WAV 文件路径
    """
    try:
        clip = VideoFileClip(input_video)
        audio_clip = clip.audio.subclip(0, 30)  # 截取前 30 秒
        audio_clip.write_audiofile(output_audio, codec='pcm_s16le')  # 采用 16-bit PCM 编码
        print(f"音频提取完成: {output_audio}")
    except Exception as e:
        print(f"提取音频时出错: {e}")

# 示例调用
extract_audio_wav("D:\\Gemini\\DemoVoice\\videoplayback.mp4", "output2.wav")

