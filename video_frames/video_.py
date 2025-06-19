import cv2
import os
def process_video(input_files,output_folder='frames'):
    """
    处理视频文件，获取信息并分解为帧
    param video_path:视频文件路径
    param output_folder:保存帧图像的文件夹
    """
    #输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap=cv2.VideoCapture("input_files/videos/input.mp4")
    if not cap.isOpened():
        print("无法打开视频文件")
        return

    frame_width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps=cap.get(cv2.CAP_PROP_FPS)
    frame_count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration=frame_count / fps

    print(f"视频信息：")
    print(f"宽度：{frame_width}像素")
    print(f"高度:{frame_height}像素")
    print(f"帧率：{fps} FPS")
    print(f"总帧数：{frame_count}")
    print(f"时长：{duration:.2f}秒")