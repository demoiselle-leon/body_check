import cv2
import os
def process_video(video_path,output_folder='../input_files/images/frames'):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    cap=cv2.VideoCapture("../input_files/videos/input.mp4")
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

    # 逐帧读取并保存
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 保存帧为图像文件
        frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_number += 1

        # 显示进度
        if frame_number % 10 == 0:
            print(f"已处理 {frame_number}/{frame_count} 帧...")

    # 释放资源
    cap.release()
    print(f"视频处理完成，共保存 {frame_number} 帧到 {output_folder} 文件夹")

if __name__ == "__main__":
    video_file = r"../input_files/videos/input.mp4"
    
    # 先检查文件是否存在
    if not os.path.exists(video_file):
        print(f"错误：视频文件不存在 - {video_file}")
    else:
        process_video(video_file)
