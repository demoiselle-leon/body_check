import cv2
import torch
from pathlib import Path
from ultralytics import YOLO


class HumanTracker:
    def __init__(self, model_path="../yolo_models/yolov8s.pt"):
        # 自动检测CUDA并初始化模型
        self.device = 0 if torch.cuda.is_available() else 'cpu'
        self.model = YOLO(model_path).to(self.device)
        print(f"Using device: {'GPU (CUDA)' if self.device != 'cpu' else 'CPU'}")

    def _get_video_writer(self, output_path, fps, width, height):
        """智能选择可用的视频编码器"""
        codecs = [
            ('avc1', 'mp4'),  # H.264 MP4
            ('mp4v', 'mp4'),  # MPEG-4
            ('XVID', 'avi'),  # AVI格式
            ('h264_nvenc', 'mp4')  # NVIDIA硬件编码
        ]

        for codec, ext in codecs:
            output_path = str(Path(output_path).with_suffix(f'.{ext}'))
            fourcc = cv2.VideoWriter_fourcc(*codec)
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            if out.isOpened():
                print(f"Using codec: {codec} -> {output_path}")
                return out
        raise RuntimeError("No available videos codec")

    def process_video(self, input_path, output_path="output"):
        # 路径标准化（兼容Windows）
        input_path = str(Path(input_path).resolve())

        # 视频输入设置
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open videos: {input_path}")

        # 获取视频参数
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # 初始化视频输出
        out = self._get_video_writer(output_path, fps, width, height)

        # 进度信息
        print(f"\nProcessing: {Path(input_path).name}")
        print(f"Resolution: {width}x{height} | FPS: {fps:.1f} | Total frames: {total_frames}")

        # 逐帧处理
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # YOLOv8 追踪（RTX 3060优化参数）
            results = self.model.track(
                frame,
                persist=True,
                classes=[0],  # 只检测人体
                imgsz=640,
                conf=0.5,
                iou=0.5,
                half=True,  # FP16加速
                device=self.device,
                verbose=False
            )

            # 绘制结果
            annotated_frame = results[0].plot(
                line_width=2,
                font_size=0.8,
                labels=True,
                boxes=True,
                masks=False
            )

            # 写入输出
            out.write(annotated_frame)
            frame_count += 1

            # 实时显示进度
            if frame_count % 10 == 0:
                print(f"\rProgress: {frame_count}/{total_frames} frames", end='')

        # 释放资源
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print(f"\n\nDone! Output saved to: {output_path}.mp4")


if __name__ == "__main__":
    tracker = HumanTracker()

    # 输入输出设置
    input_video = "../input_files/input.mp4"  # 替换为你的视频路径
    output_video = "tracked_output"  # 自动选择扩展名

    # 执行追踪
    tracker.process_video(input_video, output_video)