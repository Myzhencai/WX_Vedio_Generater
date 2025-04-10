import requests
from tqdm import tqdm


def download_video(url, output_path,count):
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
    except Exception as e:
        print(f"❌ 下载失败: {e}")


# video_url = 'https://lingtengqiu.github.io/LHM/static/videos/nazha/nazha_0.mp4'
video_url = 'https://www.youtube.com/shorts/PBpyCdy4pMg'
save_path = './Videos/'
countvalue = 1

download_video(video_url, save_path,countvalue)