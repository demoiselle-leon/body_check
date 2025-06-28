import cv2

def decode_video(input_video_path):

    cap=cv2.VideoCapture(input_video_path)
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

    return cap