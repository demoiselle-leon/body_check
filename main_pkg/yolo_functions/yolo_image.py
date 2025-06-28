import os
import cv2
from ultralytics import YOLO

def img_(input_img_path,img_name):
    # 加载模型
    current_file_path = os.path.abspath(__file__)
    model_path = os.path.join(current_file_path, '..', '..', 'yolo_models', 'yolov8s.pt')
    model = YOLO(model_path)

    # 进行预测（只检测person类，类别ID=0）
    results = model.predict(source=input_img_path, classes=[0], conf=0.5)

    # 单张图片输入
    # 返回BGR格式的numpy数组
    for r in results:
        im_array = r.plot()

    # 生成输出路径
    outfile_name = f"output_{img_name}"
    output_path = os.path.join(current_file_path, '..', '..', 'output_files', 'images', f'out_{img_name}')

    # 保存结果图像
    cv2.imwrite(output_path, im_array)
    return output_path,outfile_name