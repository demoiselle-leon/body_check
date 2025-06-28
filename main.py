from main_pkg.app_web import app
from main_pkg.yolo_functions.yolo_video import detect_and_save_video
from main_pkg.video_frames.video_ import decode_video

if __name__ == '__main__':
    app.app_()