import cv2
import streamlit as st
import time
from PIL import Image
import numpy as np

# 页面设置
st.set_page_config(layout="wide", page_title="智能检测系统")

# 初始化session状态
if 'current_page' not in st.session_state:
    st.session_state.current_page = "图片检测"

if 'img_processed' not in st.session_state:
    st.session_state.img_processed = None

if 'video_processed' not in st.session_state:
    st.session_state.video_processed = None


# 模拟处理函数
def process_image(uploaded_image):
    """模拟图片处理（实际应用中替换为你的模型）"""
    time.sleep(1)  # 模拟处理时间
    img = np.array(Image.open(uploaded_image))

    # 添加简单的处理效果 - 添加红色边界框
    processed_img = img.copy()
    cv2.rectangle(processed_img, (10, 10), (img.shape[1] - 10, img.shape[0] - 10), (255, 0, 0), 5)
    return processed_img


def process_video(uploaded_video):
    """模拟视频处理（实际应用中替换为你的模型）"""
    # 这里只是模拟处理过程
    for i in range(100):
        time.sleep(0.05)
        yield i  # 返回进度

    # 返回一个示例图片作为处理结果
    return np.random.randint(0, 255, (300, 500, 3), dtype=np.uint8)


# 页面选择器
st.sidebar.title("导航")
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
            st.image(uploaded_img, caption="原始图片", use_column_width=True)

    with col2:
        st.subheader("检测结果")
        if st.session_state.img_processed is not None:
            st.image(st.session_state.img_processed, caption="处理后的图片", use_column_width=True)
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
                st.session_state.img_processed = process_image(uploaded_img)
                st.success("处理完成!")
                st.rerun()

# 视频检测页面
elif page == "视频检测":
    st.header("视频检测系统")

    # 创建两列布局
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("上传视频")
        uploaded_video = st.file_uploader("选择视频文件", type=["mp4", "mov"], key="video_upload")
        if uploaded_video:
            st.video(uploaded_video)

    with col2:
        st.subheader("检测结果")
        if st.session_state.video_processed is not None:
            st.image(st.session_state.video_processed, caption="处理后的视频帧", use_column_width=True)
        else:
            st.info("上传视频后点击开始识别")

    # 底部控制区域
    st.divider()
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        if st.button("开始识别", key="video_button", disabled=not uploaded_video):
            with st.spinner("处理中..."):
                progress_bar = st.progress(0)

                # 处理视频并显示进度
                for progress in process_video(uploaded_video):
                    progress_bar.progress(progress + 1)

                # 模拟处理结果
                st.session_state.video_processed = np.random.randint(0, 255, (300, 500, 3), dtype=np.uint8)
                st.success("处理完成!")
                st.rerun()