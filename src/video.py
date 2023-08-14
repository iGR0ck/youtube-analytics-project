from src.channel import Channel
import os


# ключ для переменной окружения
YOUTUBE_API_KEY: str = os.getenv('YT_API_KEY')


class Video:

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.title = None
        self.url = None
        self.view_count = None
        self.like_count = None
        self.correct_id()


    def __str__(self):
        """
        Выводит название видео
        """
        return f'{self.title}'

    def correct_id(self):
        """
        Метод проверяет можно ли получить данные о видео,
        если нет то выводит: Exception error
        """
        try:
            youtube = Channel.get_service().videos().list(part='snippet,statistics', id=self.video_id).execute()
            video_data = youtube.get('items')[0]
            self.title = video_data.get('snippet').get('title')
            self.url = f'https://www.youtube.com/watch?v={self.video_id}'
            self.view_count = int(video_data.get('statistics').get('viewCount'))
            self.like_count = int(video_data.get('statistics').get('likeCount'))
        except Exception:
            print('Exception error : Невозможно получить данные о видео')


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id