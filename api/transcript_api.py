from youtube_transcript_api import YouTubeTranscriptApi

def fetch_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        transcript_data = transcript.fetch()
        script = "\n".join([t['text'] for t in transcript_data])
        return script
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None
