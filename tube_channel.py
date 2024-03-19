''' 한 채널의 영상 모두 다운로드 / 구글 API 필요

한 채널의 영상 모두 다운받기
1. YOUTUBE DATA API KEY 발급
채널에 포함된 영상의 리스트를 얻기 위해서 YouTube Data API v3 를 사용합니다. 이 API를 사용하려면 API Key가 필요하므로 API Key가 없다면 다음과 같이 YouTube API를 받을 수 있습니다.

Google 개발자 콘솔로 이동합니다.
상단 탐색 모음에서 "프로젝트 선택" 드롭다운 메뉴를 클릭한 다음 "새 프로젝트" 버튼을 클릭하여 새 프로젝트를 만듭니다.
프로젝트 이름을 입력하고 "만들기"를 클릭합니다.
프로젝트가 생성되면 "프로젝트 선택" 드롭다운 메뉴에서 프로젝트를 선택합니다.
"API 및 서비스 활성화" 버튼을 클릭하고 "YouTube 데이터 API"를 검색하여 YouTube 데이터 API를 활성화합니다. API를 클릭한 다음 "활성화" 버튼을 클릭합니다.
"자격증명 만들기" 버튼을 클릭하고 "API 키"를 선택하여 프로젝트에 대한 자격 증명을 만듭니다. 프롬프트에 따라 API 키를 생성합니다.
경우에 따라 YouTube Data API를 사용하려면 OAuth 2.0 자격 증명을 설정해야 할 수 있습니다. 이렇게 하려면 "자격증명 만들기" 버튼을 클릭하고 "OAuth 클라이언트 ID"를 선택합니다. 안내에 따라 OAuth 클라이언트 ID를 만듭니다.
API 키 및/또는 OAuth 2.0 자격 증명이 있으면 이를 사용하여 YouTube API에 대한 요청을 인증할 수 있습니다.
2. 코드
아래는 YouTube 채널의 모든 shorts 동영상을 다운로드받는 코드입니다. 채널 ID를 인수로 사용하고 채널의 업로드 재생 목록을 검색한 다음 "Shorts" 동영상으로 분류된 동영상을 다운로드하는 샘플 코드입니다.

아래 예시에서는 다운받을 영상을 채널 및 shorts 영상으로 제한했지만 코드를 응용하면 다른 조건의 영상들도 한번에 받을 수 있습니다.

yt.streams.filter()를 사용하여 영상 퀄리티를 조정할 수 있습니다. 아래에서는 최상의 품질로 다운받습니다.

'''
import os
import google.auth
from googleapiclient.discovery import build
from pytube import YouTube


credentials = 'AIzaSyDTLUB3oB-l4KetTfaG4DGEyw4bOElr8Iw'

def download_shorts(channel_id):
    # Authenticate with YouTube Data API
    credentials, project = google.auth.default()
    youtube = build('youtube', 'v3', credentials=credentials)

    # Retrieve channel's uploads playlist
    channel_response = youtube.channels().list(part='contentDetails', id=channel_id).execute()
    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Retrieve playlist items and download "short" videos
    playlistitems_request = youtube.playlistItems().list(part='snippet', playlistId=uploads_playlist_id, maxResults=50)
    while playlistitems_request is not None:
        playlistitems_response = playlistitems_request.execute()
        for playlist_item in playlistitems_response['items']:
            video_id = playlist_item['snippet']['resourceId']['videoId']
            video_response = youtube.videos().list(part='snippet', id=video_id).execute()
            video_tags = video_response['items'][0]['snippet']['tags']
            if 'Shorts' in video_tags: # 쇼츠만 다운르드
                print(f'Downloading {video_id}')
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                yt = YouTube(video_url)
                yt.streams.filter(adaptive=True, file_extension='mp4').first().download()
        playlistitems_request = youtube.playlistItems().list_next(playlistitems_request, playlistitems_response)

if __name__ == '__main__':
    channel_id = 'INSERT_YOUTUBE_CHANNEL_ID_HERE'
    download_shorts(channel_id)

'''
3. 코드 실행
위 코드를 video_download.py로 저장하고, 터미널에 다음과 같이 실행하면 영상이 받아집니다.

cd {파일이 저장된 디렉토리}
python3 ./video_downlaod.py {채널ID}
'''