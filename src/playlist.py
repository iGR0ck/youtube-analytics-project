from datetime import timedelta
from src.channel import Channel
import os
import isodate


class PlayList:
    api_key = os.getenv('API_YOUTUBE')

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = None
        self.url = None
        self.videos = []
        self.video_data()

    def video_data(self):
        youtube = Channel.get_service().playlistItems().list(playlistId=self.playlist_id, part='snippet,contentDetails,id,status', maxResults=10,).execute()
        playlist_data = youtube.get('items')[0]
        self.title = playlist_data.get('snippet').get('title').split(".")[0]
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

        video_ids = [video['contentDetails']['videoId'] for video in youtube['items']]
        videos = Channel.get_service().videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)
        ).execute()
        self.videos = videos.get('items')

    @property
    def total_duration(self):
        total = timedelta()
        for video in self.videos:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        best_video = max(self.videos, key=lambda video: video.get('statistics').get('likeCount'))
        return f"https://youtu.be/{best_video['id']}"