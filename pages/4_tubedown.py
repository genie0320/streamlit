# pip install pytube
# pip install -qU streamlit streamlit-extras

"""
:red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
:gray[pretty] :rainbow[colors].

"""

import streamlit as st
from pytube import YouTube as yt
import re

st.title(":red[Youtube] downloader :sunglasses:")


@st.cache_data
def get_video(url):
    source = yt(url)
    streams = source.streams
    return (source, streams)


user_input = st.text_input("1. Set URL", placeholder="http://")

if len(user_input) < 8:
    st.info("Set URL please.")
else:
    # with st.spinner():
    if "source" not in st.session_state or st.session_state.source != user_input:
        st.session_state.source, st.session_state.stream = get_video(user_input)
    source = st.session_state.source
    stream = st.session_state.stream
    st.success(f"[ {source.title} ]영상이 준비되었습니다.")
    st.image(source.thumbnail_url)
    option = stream.filter(progressive=True).order_by("resolution").desc()

    # 해상도 선택 셀렉트 박스
    _option = st.selectbox(
        "다운로드 하실 해상도를 선택해주세요.",
        option,
        index=None,
        placeholder="해상도 선택",
    )

    if st.button("Download", type="primary"):
        tag = re.search(r'itag="(\d+)', str(_option)).group(1)
        target = stream.get_by_itag(tag)
        target.download(filename=f"{source.title}.mp4", output_path="downloads/")
        st.success("Download Complete", icon="✅")

    if st.button("Reset", type="secondary"):
        st.empty()
