from googleapiclient.discovery import build
import os


# ключ для переменной окружения
YOUTUBE_API_KEY: str = os.getenv('YT_API_KEY')


class Video:

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.title = self.video_info["items"][0]["snippet"]["title"]
        self.url = self.video_info["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        self.view_count = self.video_info["items"][0]["statistics"]["viewCount"]
        self.like_count = self.video_info["items"][0]["statistics"]["likeCount"]


    def __str__(self):
        """
        Выводит название видео
        """
        return f'{self.title}'


    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        # объект для работы с API
        cls.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        return cls.youtube


    @property
    def video_info(self):
        """
        Возвращает информацию по видео.
        """
        video = Video.get_service().videos().list(id=self.video_id, part='snippet,statistics').execute()
        return video


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id