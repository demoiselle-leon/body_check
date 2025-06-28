import os
import streamlit as st
import time
from PIL import Image
import numpy as np

from ..yolo_functions.yolo_image import img_
from ..video_frames.video_ import decode_video
from ..yolo_functions.yolo_video import detect_and_save_video

def app_():
    # 页面设置
    st.set_page_config(layout="wide", page_title="智能人体检测系统")

    # 初始化session状态为图片检测
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "图片检测"
    if 'img_processed' not in st.session_state:
        st.session_state.img_processed = None
    if 'video_processed' not in st.session_state:
        st.session_state.video_processed = None


    # 处理函数
    def process_image(image_save_path,img_name):
        outfile_path=img_(image_save_path,img_name)[0]
        img = Image.open(outfile_path)
        return img


    def process_video(video_save_path,video_name):
        model_path = os.path.join(current_file_path, '..', '..', 'yolo_models', 'yolov8s.pt')
        out_path = detect_and_save_video(decode_video(video_save_path), model_path,video_name)
        return out_path


    # 页面选择器
    st.sidebar.title("智能人体识别系统")
    page = st.sidebar.radio("选择检测类型", ["图片检测", "视频检测"])

    # 图片检测页面
    if page == "图片检测":
        st.header("图片检测系统")

        # 创建两列布局
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("上传图片")
            uploaded_img = st.file_uploader("选择图片文件", type=["jpg", "jpeg", "png"], key="img_upload")
            if uploaded_img:
                # 保存图片到本地
                current_file_path = os.path.abspath(__file__)
                sava_img_path = os.path.join(current_file_path, '..', '..', 'input_files', 'images', f'{uploaded_img.name}')
                with open(sava_img_path , "wb") as f:
                    f.write(uploaded_img.getbuffer())
                st.image(uploaded_img, caption="原始图片", use_container_width=True)

        with col2:
            st.subheader("检测结果")
            if st.session_state.img_processed is not None:
                st.image(st.session_state.img_processed, caption="处理后的图片", use_container_width=True)
            else:
                st.info("上传图片后点击开始识别")

        # 底部控制区域
        st.divider()
        _, center_col, _ = st.columns([1, 2, 1])

        with center_col:
            if st.button("开始识别", key="img_button", disabled=not uploaded_img):
                with st.spinner("处理中..."):
                    progress_bar = st.progress(0)

                    # 模拟处理进度
                    for percent_complete in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(percent_complete + 1)

                    # 处理图片
                    st.session_state.img_processed = process_image(sava_img_path,uploaded_img.name)
                    st.success("处理完成!")
                    st.rerun()

    # 视频检测页面
    elif page == "视频检测":
        pass
        st.header("视频检测系统")

        # 创建两列布局
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("上传视频")
            uploaded_video = st.file_uploader("选择视频文件", type=["mp4", "mov"], key="video_upload")
            if uploaded_video:
                # 保存视频到本地
                current_file_path = os.path.abspath(__file__)
                sava_video_path = os.path.join(current_file_path, '..', '..', 'input_files', 'videos',f'{uploaded_video.name}')
                with open(sava_video_path,'wb') as f:
                    f.write(uploaded_video.getbuffer())
                st.video(uploaded_video)

        with col2:
            st.subheader("检测结果")
            if st.session_state.video_processed is not None:
                st.video(st.session_state.video_processed)
            else:
                st.info("上传视频后点击开始识别")

        # 底部控制区域
        st.divider()
        _, center_col, _ = st.columns([1, 2, 1])

        with center_col:
            if st.button("开始识别", key="video_button", disabled=not uploaded_video):
                with st.spinner("处理中..."):

                    # 模拟处理结果
                    st.session_state.video_processed = process_video(sava_video_path,uploaded_video.name)
                    st.success("处理完成!")
                    st.rerun()