import os

import cv2
import torch
from ultralytics import YOLO
from pathlib import Path


def detect_and_save_video(cap, model_path, file_name):
    current_file_path = os.path.abspath(__file__)
    out_path = os.path.join(current_file_path, '..', '..', 'output_files', 'images', f'out_{file_name}')
    # 检查输出路径是否有效
    if Path(out_path).is_dir():
        raise ValueError("输出路径必须是文件路径（如'output.mp4'），不能是目录")

    # 加载YOLOv8模型
    model = YOLO(model_path)

    # 获取视频信息
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 创建视频写入器（使用H264编码需要额外配置）
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    if not out.isOpened():
        raise IOError(f"无法创建输出视频文件: {out_path}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # YOLOv8推理
        results = model(frame, verbose=False)

        # 绘制检测框
        for result in results:
            for box in result.boxes:
                if box.cls == 0 and box.conf > 0.5:  # 人体类别0，置信度>0.5
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    conf = float(box.conf)  # 将Tensor转为float

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'person {conf:.2f}', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 写入输出视频
        out.write(frame)

    # 释放资源
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"处理完成，结果已保存到: {out_path}")
    return out_path