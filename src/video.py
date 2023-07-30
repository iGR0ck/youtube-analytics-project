from googleapiclient.discovery import build
import os


# ключ для переменной окружения
YOUTUBE_API_KEY: str = os.getenv('YT_API_KEY')


class Video:

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id


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

    @property
    def title(self):
        """
        Показывает заголовок видео
        """
        return self.video_info["items"][0]["snippet"]["title"]

    @property
    def url(self):
        """
        Показывает ссылку на видео
        """
        return self.video_info["items"][0]["snippet"]["thumbnails"]["default"]["url"]

    @property
    def view_count(self):
        """
        Показывает кол-во просмотров
        """
        return self.video_info["items"][0]["statistics"]["viewCount"]

    @property
    def like_count(self):
        """
        Показывает кол-во лайков
        """
        return self.video_info["items"][0]["statistics"]["likeCount"]


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str) -> None:
        self.video_id = video_id
        self.playlist_id = playlist_id
        self.__title = super().title
        self.__url = super().url
        self.__view_count = super().view_count
        self.__like_count = super().like_count
