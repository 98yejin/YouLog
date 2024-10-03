from googleapiclient.discovery import build


def search_videos(query, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # First, perform a search to get video IDs
    search_request = youtube.search().list(
        q=query,
        part='id',
        type='video',
        maxResults=50  # Increase to get more videos to filter
    )
    search_response = search_request.execute()

    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]

    if not video_ids:
        return []

    # Now, get video details and filter by captions
    videos_request = youtube.videos().list(
        part='snippet,contentDetails',
        id=','.join(video_ids),
        maxResults=50
    )
    videos_response = videos_request.execute()

    video_items = []
    for item in videos_response.get('items', []):
        captions_available = 'caption' in item['contentDetails'] and item['contentDetails']['caption'] == 'true'
        if captions_available:
            title = item['snippet']['title']
            video_id = item['id']
            video_items.append(f"{title} ({video_id})")

    return video_items