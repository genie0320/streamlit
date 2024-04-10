# pip install pytube
# pip install -qU streamlit streamlit-extras

"""
:red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
:gray[pretty] :rainbow[colors].

"""

# from pytube import YouTube as yt
import streamlit as st
import re
import os
import pyautogui
import webbrowser
import myTube as tube
import myGemini as genai

st.title(":red[Youtube] downloader :sunglasses:")


# def clear_state():
#     for key in st.session_state.keys():
#         del st.session_state[key]
#     pyautogui.hotkey("ctrl", "f5")


# st.button("Clear", on_click=clear_state)


# @st.cache_data
def get_ready(url):
    st.session_state = tube.get_source(user_input)
    st.header("init")


# "https://youtu.be/xPA0LFzUDiE?si=-dgYEVwBCuKUah-Q"

user_input = st.text_input("1. Set URL", placeholder="http://")


if len(user_input) < 8:
    st.info("Set URL please.")

else:
    # if "source" not in st.session_state :
    if "source" not in st.session_state.keys() or st.session_state["url"] != user_input:
        get_ready(user_input)
        # st.write(tube.get_source(user_input))

    source = st.session_state["source"]
    v_stream = st.session_state["v_streams"]
    a_stream = st.session_state["a_streams"]
    # Details Fold
    with st.expander("다운로드 할 영상을 확인해주세요."):
        col1, col2 = st.columns([1, 2])
        col1.image(source.thumbnail_url)
        infos = (
            f"**{source.title}**" + "\n"
            f"- 채널명 : [**{source.author}**]({source.channel_url})"
            + "\n"
            + f"- 업로드 일자 : {source.publish_date}"
            + "\n"
            + f"- 재생시간 : 약 {int(source.length / 60)} 분"
            + "\n"
            + f"- 좋아요 : {'{:,}'.format(source.views)}"
        )
        col2.markdown(infos)

    # Start tab ui
    tab1, tab2, tab3 = st.tabs(["Video Downloader", "Audio Downloader", "Summarizer"])

    # Downloader
    with tab1:

        v_option = st.selectbox(
            "다운로드 하실 해상도를 선택해주세요.",
            v_stream,
            index=None,
            placeholder="해상도 선택",
        )

        if st.button("Download", type="primary"):
            tag, _ = tube.get_itag(v_option)
            target = source.streams.get_by_itag(tag)
            user_download_folder = os.path.expanduser("~/Downloads")
            target.download(
                filename=f"{source.title}.mp4", output_path=user_download_folder
            )
            st.success("Download Complete", icon="✅")
            webbrowser.open("file://" + user_download_folder)

    with tab2:
        a_option = st.selectbox(
            "다운로드 하실 음질을 선택해주세요.",
            a_stream,
            index=None,
            placeholder="음질 선택",
        )

        if st.button("Download"):
            tag, extention = tube.get_itag(a_option)
            target = source.streams.get_by_itag(tag)
            user_download_folder = os.path.expanduser("~/Downloads")

            target.download(
                filename=f"{source.title}.{extention}", output_path=user_download_folder
            )
            st.success("Download Complete", icon="✅")
            webbrowser.open("file://" + user_download_folder)

    with tab3:
        script = "스크립트를 가져와주세요."
        if st.button("스크립트 가져오기"):
            vid_id = tube.get_id(source)
            script = tube.get_script(vid_id)
            container = st.container(height=300, border=True)
            container.write(script)
            sum = genai.get_summary(script)
            container.write(sum)
