from pytube import YouTube


def get_source(urls):
    """
    - 주어진 URL로 youtube 객체를 만들어 돌려준다.

    :progressive=True,  # 720p까지. 소리/영상 일체본
    :adaptive=False,  # 고화질. but 소리/영상 따로
    :audio_only=False,
    :file_extension="mp4",
    :high_quality=False,
    """

    # yt = YouTube(urls)
    return YouTube(urls)
    # opt = yt.streams.filter(
    #     file_extension=file_extension,
    #     progressive=progressive,
    #     adaptive=adaptive,
    #     only_audio=only_audio,
    # )
    # return opt.order_by("resolution")
    # print(yt.streams.filter(progressive=True).order_by("resolution")[-1])
    # target = yt.streams.filter(progressive=True).order_by("resolution")[-1]
    # target.download()


urls = "http://youtube.com/watch?v=2lAe1cqCOXo"

source = get_source(urls)
source.title
thumb = source.thumbnail_url
thumb

downloadable = source.streams
downloadable
type(downloadable)  # pytube.query.StreamQuery

downloadable.filter(only_audio=True, file_extension='mp4').desc()
downloadable.filter(progressive=True).desc()[0]
v = downloadable.filter(progressive=True).desc()
len(v)

_v = list(enumerate(v))
_v[0][1]

for k, v in enumerate(v):
    if v == '<Stream: itag="22" mime_type="video/mp4" res="720p" fps="24fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">':
        print(k)


from _streamlit-tutorial-main.01-data import values
v = downloadable.filter(progressive=True).desc()[0]
re.search(r'itag')


# [
#     <Stream: itag="139" mime_type="audio/mp4" abr="48kbps" acodec="mp4a.40.5" progressive="False" type="audio">, 
#     <Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2" progressive="False" type="audio">, 
#     <Stream: itag="249" mime_type="audio/webm" abr="50kbps" acodec="opus" progressive="False" type="audio">, 
#     <Stream: itag="250" mime_type="audio/webm" abr="70kbps" acodec="opus" progressive="False" type="audio">, 
#     <Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="opus" progressive="False" type="audio">
#     ]