# !pip install -q pytube
# https://console.developers.google.com/
# AIzaSyDTLUB3oB-l4KetTfaG4DGEyw4bOElr8Iw

from pytube import YouTube

def download_video(video_url):
    yt = YouTube(video_url)
    yt.streams.filter(
        res='720p', 
        # adaptive=True, 
        progressive = True,
        file_extension='mp4',
        ).first().download()

if __name__ == '__main__':
    video_url = [
        # 'https://youtu.be/jl5ahJ4vD8w?si=rThLV1_FyAAZ4FXA',
        'https://youtu.be/WOmUA7THTXg?si=u4CSVkk29ByDBtVF',
        'https://youtu.be/MlAPAyZrUD0?si=lfWlC3Gpuxwu_sge',
        'https://youtu.be/Ny-Az8nAAaM?si=0sj-zkCI5H9Z-HC4',
        'https://youtu.be/54RqkHphIB8?si=clc5WUsElSfKRZ5N',
        'https://youtu.be/VB1OAhjLZXs?si=df5kOZtQ80m_usCr',
        'https://youtu.be/FwELc83oPz8?si=52mp_FPESKiDPPaI'
        ]
    # download_video(video_url)
    for url in video_url:
        download_video(url)

print('All Done')

# python ./video_downlaod.py
# python ./tubedown.py
    

'''
resolution (str): 동영상 해상도 ('144p', '240p', '360p', '480p', '720p', '1080p', ...)
file_extension (str): 동영상 파일 형식 ('mp4', 'webm', ...)
progressive (bool): 다운로드 가능한 전체 동영상 파일에 대한 스트림 필터링
adaptive (bool): 세그먼트화 된 스트리밍 동영상에 대한 스트림 필터링
only_audio (bool): 오디오 파일에 대한 스트림 필터링
mime_type (str): 파일의 MIME 유형
'''    