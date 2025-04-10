import os
import shutil

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

# 示例用法
clear_folder("./Videos")