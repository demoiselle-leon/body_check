
### 校园安全监控视频异常事件检测
###### version: 1.0
###### 项目成员：朱来勋，陈小林，刁源，杨亮

#### 程序模块
1.app_web：webAPI，使用streamLit实现前端UI，用户上传数据存入input_file,处理结束后读取对应output_files中数据文件，显示给用户

2.video_frames：取出input_files中的视频进行解码（获得视频帧率、帧数、高度、宽度），为yolo_functions模块传递图片帧变量

3.yolo_functions：算法1：人体追踪视频识别（处理数据帧，绘制标记，重组视频，存入output_files）算法2：人体图像识别（读取input_files图片数据，处理，存入output_files）

4.main.py
#### 数据模块
1.input_files（存取用户输入数据.mp4/.png）

2.output_files（存取用户输出数据.mp4/.png）

3.yolo_models（存取模型文件.pt）

### 注：test模块为测试模块
