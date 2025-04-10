# import requests
#
#
# def download_video(url: str, save_path: str):
#     """
#     下载视频并保存到指定路径。
#
#     :param url: 视频的 URL 地址。
#     :param save_path: 本地保存路径（包括文件名）。
#     """
#     try:
#         import requests  # 确保 requests 已导入
#         response = requests.get(url, stream=True)
#         response.raise_for_status()
#
#         with open(save_path, 'wb') as file:
#             for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB 块大小
#                 if chunk:
#                     file.write(chunk)
#
#         print(f"视频下载完成: {save_path}")
#     except requests.RequestException as e:
#         print(f"下载失败: {e}")
#
#
# # 示例用法
# download_video("https://lingtengqiu.github.io/LHM/static/videos/nizaichangge/nizaichangge_1.mp4", "nizaichangge_1.mp4")


import requests
import os




def download_video(url: str, save_path: str):
    """
    下载视频并保存到指定路径。

    :param url: 视频的 URL 地址。
    :param save_path: 本地保存路径（包括文件名）。
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB 块大小
                if chunk:
                    file.write(chunk)

        print(f"视频下载完成: {save_path}")
    except requests.RequestException as e:
        print(f"下载失败: {e}")


def download_videos_from_txt(txt_file: str, save_folder: str):
    """
    从 TXT 文件中读取 URL 并下载视频。

    :param txt_file: 包含视频 URL 的 TXT 文件。
    :param save_folder: 存储视频的文件夹。
    """
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    with open(txt_file, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file if line.strip()]

    for index, url in enumerate(urls, start=1):
        save_path = os.path.join(save_folder, f"{index}.mp4")
        download_video(url, save_path)


# 示例用法
download_videos_from_txt("SourceFile/urls.txt", "./Videos")