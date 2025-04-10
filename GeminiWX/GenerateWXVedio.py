# 1.从提供的txt连接文档里面去下载视频保存到Videos
# 2.从提供的txt对应的文本信息输入到gemini自动生成新的文本
# 3.将新的文本生成语音文件
# 4.将视频文件压缩到10秒，将文本压缩到10秒，并融合成新视频保存
import os
import yt_dlp
import shutil
import requests
import torchaudio
from tqdm import tqdm
from google import genai
from DownloadX import downloadx
from moviepy.video.fx import all as fx
from FireRedTTS.GenerateVoice import generageVoicemodel
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip, concatenate_videoclips,AudioFileClip

def detect_url_source(url: str) -> int:
    """
    检测 URL 来源
    :param url: 要检测的链接
    :return: 1 - YouTube, 2 - X.com, 3 - 其他
    """
    if "https://www.youtube.com" in url:
        return 1
    elif "https://x.com" in url:
        return 2
    else:
        return 3


def download_youtube_video(url, save_path='./', count=0):
    """
    使用 yt_dlp 下载 YouTube 视频，并重命名为固定格式
    :param url: 视频链接
    :param save_path: 保存路径
    :param count: 视频编号（用于生成文件名）
    """
    # 确保保存路径存在
    os.makedirs(save_path, exist_ok=True)

    # 构建保存文件名，例如：./Videos/0001.mp4
    filename = f"{int(count)}.mp4"
    output_template = os.path.join(save_path, filename)

    ydl_opts = {
        'outtmpl': output_template,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print(f"下载完成：{filename}")
        except Exception as e:
            print(f"下载失败：{e}")


def download_videompfour(url, output_path,count):
    """
    下载视频文件到本地

    参数:
    - url: 视频链接（必须是可直接访问的链接）
    - output_path: 保存视频的本地路径，例如 'video.mp4'
    """

    output_path = output_path + f"{count}.mp4"
    try:
        # 发起请求，开启流模式
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        # 获取文件总大小（用于显示进度条）
        total_size = int(response.headers.get('content-length', 0))

        # 下载并写入文件
        with open(output_path, 'wb') as f, tqdm(
                desc=output_path,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
        print("✅ 下载完成！")
        return 1
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return 0


def merge_videos(a_path, b_path, output_path="output.mp4"):
    # 加载A视频
    clip_a = VideoFileClip(a_path,audio=False).resize((720, 1280))

    # 创建纯黑色区域（720x540）
    black_box = ColorClip(size=(720, 540), color=(0, 0, 0), duration=clip_a.duration)
    black_box = black_box.set_position(("center", "center"))

    # 加载B视频，宽度设为710，高度等比缩放
    clip_b = VideoFileClip(b_path,audio=False)
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

def clear_folder(folder_path):
    # 确保路径存在
    if os.path.exists(folder_path):
        # 遍历文件夹中的文件并删除
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # 如果是文件，删除它
                if os.path.isfile(file_path):
                    os.remove(file_path)
                # 如果是文件夹，递归删除
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"删除 {file_path} 时出错: {e}")
    else:
        print(f"文件夹 {folder_path} 不存在")


# 合成视频
def merge_video_audio_files(video_dir, audio_dir, output_dir):
    """
    遍历 video_dir 和 audio_dir，将具有相同前缀的 MP4 视频和 WAV 音频合成新视频，并保存到 output_dir。

    :param video_dir: 存放视频文件的目录
    :param audio_dir: 存放音频文件的目录
    :param output_dir: 输出合成后视频的目录
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
        print(AudioFileClip(audio_path).duration)
        try:
            video = VideoFileClip(video_path).subclip(0, min(AudioFileClip(audio_path).duration, AudioFileClip(audio_path).duration))
            audio = AudioFileClip(audio_path).subclip(0, min(AudioFileClip(audio_path).duration, AudioFileClip(audio_path).duration))

            final_video = video.set_audio(audio)
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
        except Exception as e:
            print(f"合并 {prefix} 失败: {e}")

# 文本转语音
def text_to_speech(text_file, output_dir="./output_wavs"):
        tts = generageVoicemodel()

        os.makedirs(output_dir, exist_ok=True)

        with open(text_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

        for i, line in enumerate(lines):
                line = line.strip('\n')
                if not line:
                        continue

                rec_wavs = tts.synthesize(
                        # prompt_wav="D:\\Gemini\\FireRedTTS\\examples\\prompt_1.wav",
                        prompt_wav="D:\\Gemini\\output2.wav",
                        text=line,
                        lang="zh",
                )
                rec_wavs = rec_wavs.detach().cpu()

                output_path = os.path.join(output_dir, f"{i + 1}.wav")
                torchaudio.save(output_path, rec_wavs, 24000)

        return output_dir

# 下载X视频
def download_videos_from_file(file_path):
    downloader = downloadx()
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
        count = 1
        for url in urls:
            url = url.strip()
            if url:
                # 根据url来下载
                downloadtype = detect_url_source(url)
                if downloadtype ==1:
                    download_youtube_video(url, save_path='./Videos/', count=count)
                    count += 1
                elif downloadtype ==2:
                    downloader.download_video(url, count)
                    count += 1
                else:
                    download_videompfour(url, output_path='./Videos/', count=count)
                    count +=1
            else:
                print("Skipping empty line.")
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Gemini重写内容
def rewrite(input_path: str, output_path: str):
    client = genai.Client(api_key="AIzaSyDnJ-HAfTYa7hdO4V2xXhuIAbElsjfxtSI")

    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    processed_lines = []
    for line in lines:
        content = line.strip().replace(";", "")
        prompt = f"翻译:{content}"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        prompt2 = f"重写成微信小视频的180个字描述，内容意思不变，不要出现问号，只需要一个最好的回复:{response.text}"
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt2,
        )

        # processed_lines.append(content)
        processed_lines.append(response.text)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(processed_lines)

    print(f"处理完成，结果已保存到 {output_path}")

def merge_video_audio_files_fast(video_dir, audio_dir, output_dir, target_duration=18):
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

def download_video(url: str, save_path: str):
    """
    下载视频并保存到指定路径。

    :param url: 视频的 URL 地址。
    :param save_path: 本地保存路径（包括文件名）。
    """
    try:
        import requests  # 确保 requests 已导入
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB 块大小
                if chunk:
                    file.write(chunk)

        print(f"视频下载完成: {save_path}")
    except requests.RequestException as e:
        print(f"下载失败: {e}")


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




# clear_folder("./Videos")
# clear_folder("./OutV")
# clear_folder("./Tempfiles")
# clear_folder("./output_wavs")

# # 视频链接地址
# Xpostlinks = "SourceFile/urls.txt"
# download_videos_from_file(Xpostlinks)

# # 描述内容地址
Xcontant = 'SourceFile/cotant.txt'
rewrite(Xcontant, 'Tempfiles/cotant_processed.txt')
#
# # 内容转语音
text_to_speech("Tempfiles/cotant_processed.txt", output_dir="./output_wavs")

# 合成标准模版视频
batch_merge_videos(
    a_path="rotated_video.mp4",
    b_folder_path="./Videos",
    output_folder_path="./MergeVideos"
)

#合成视频
merge_video_audio_files("./MergeVideos", "./output_wavs", "./OutV")
# merge_video_audio_files_fast("./Videos", "./output_wavs", "./OutV")



