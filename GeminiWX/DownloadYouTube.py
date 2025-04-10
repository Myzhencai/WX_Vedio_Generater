from pytube import YouTube

def download_youtube_video(url, save_path='./', resolution='720p'):
    """
    下载指定 YouTube 视频
    :param url: 视频链接
    :param save_path: 保存路径（默认当前目录）
    :param resolution: 视频分辨率，默认720p
    """
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', res=resolution).first()

        if not stream:
            print(f"未找到 {resolution} 分辨率的视频，尝试下载最高质量视频。")
            stream = yt.streams.get_highest_resolution()

        print(f"正在下载：{yt.title}")
        stream.download(output_path=save_path)
        print("下载完成！")
    except Exception as e:
        print(f"下载失败：{e}")

import yt_dlp

# def download_youtube_video2(url, save_path='./'):
#     """
#     使用 yt_dlp 下载 YouTube 视频
#     :param url: 视频链接
#     :param save_path: 保存路径
#     """
#     ydl_opts = {
#         'outtmpl': f'{save_path}/%(title)s.%(ext)s',
#         'format': 'bestvideo+bestaudio/best',
#         'merge_output_format': 'mp4'
#     }
#
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             ydl.download([url])
#             print("下载完成！")
#         except Exception as e:
#             print(f"下载失败：{e}")

import yt_dlp
import os

def download_youtube_video2(url, save_path='./', count=0):
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


# download_youtube_video2("https://www.youtube.com/watch?v=C2BTnx6swf4", save_path="./Videos", resolution='720p')
download_youtube_video2("https://www.youtube.com/shorts/pS-fFdvyHLE", save_path="./Videos",count=15)
