import cv2

# 打开原始视频
input_path = 'Flip.mp4'
cap = cv2.VideoCapture(input_path)

# 获取原视频的属性
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 注意宽高互换
height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 选择合适的编码器
output_path = 'rotated_video.mp4'
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# 逐帧读取、旋转、写入
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 顺时针旋转90度
    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    out.write(rotated_frame)

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()
