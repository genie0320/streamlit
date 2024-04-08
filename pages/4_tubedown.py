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

st.title(":red[Youtube] downloader :sunglasses:")
st.write(st.session_state)


def clear_state():
    for key in st.session_state.keys():
        del st.session_state[key]
    pyautogui.hotkey("ctrl", "f5")


st.button("Clear", on_click=clear_state)


@st.cache_data
def get_ready(url):
    with st.sidebar:
        print(tube.get_source(url))
    return tube.get_source(url)


"https://youtu.be/xPA0LFzUDiE?si=-dgYEVwBCuKUah-Q"

user_input = st.text_input("1. Set URL", placeholder="http://")

if len(user_input) < 8:
    st.info("Set URL please.")

else:
    if "source" not in st.session_state or st.session_state.source["url"] != user_input:
        st.session_state.source = get_ready(user_input)
        st.write(st.session_state)
        # st.write(get_ready(user_input))

    _source = st.session_state.source
    source = st.session_state.source["source"]
    v_stream = _source["v_streams"]
    a_stream = _source["a_streams"]
    st.write(a_stream)
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
    tab1, tab2, tab3 = st.tabs(["Downloader", "Summarizer", "Etc"])

    # Downloader
    with tab1:

        v_option = st.selectbox(
            "다운로드 하실 해상도를 선택해주세요.",
            v_stream,
            index=None,
            placeholder="해상도 선택",
        )

        if st.button("Download", type="primary"):
            tag = tube.get_itag(v_option)
            target = source.get_by_itag(tag)
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
            target = source.get_by_itag(tag)
            user_download_folder = os.path.expanduser("~/Downloads")
            
            extention = 
            target.download(
                filename=f"{source.title}.mp4", output_path=user_download_folder
            )
            st.success("Download Complete", icon="✅")
            webbrowser.open("file://" + user_download_folder)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
