# %%
# AIzaSyBa0ZJ1BBxpVNe6vPrmQ3rzMpzI4ksdY_U

from googleapiclient.discovery import build


def youtube_search(keyword, max_results=10):
    # Replace with your API key
    DEVELOPER_KEY = "AIzaSyBa0ZJ1BBxpVNe6vPrmQ3rzMpzI4ksdY_U"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )

    # Search request
    search_response = (
        youtube.search()
        .list(part="snippet", q=keyword, type="video", maxResults=max_results)
        .execute()
    )

    # Extract video information
    videos = []
    for item in search_response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        view_count = item["snippet"]["thumbnails"]["default"]["url"].split("/")[-2]

        videos.append({"id": video_id, "title": title, "view_count": view_count})

    return videos


# Example usage
keyword = "cats"  # Replace with your desired keyword
search_results = youtube_search(keyword)

for video in search_results:
    print(f"Title: {video['title']}")
    print(f"View Count: {video['view_count']}")
    print("---")
