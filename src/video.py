from src.channel import Channel


class Video(Channel):

    def __init__(self, video_id: str) -> None:
        self.id = video_id
        # переназначаю аргумент с channel_info на video_info от родительского класса для удобства его вызова
        self.video_info = self.channel_info

    def __str__(self):
        """
        Выводит название видео
        """
        return f'{self.title}'

    @property
    def channel_info(self):
        """
        Возвращает информацию по видео.
        """
        video = Video.get_service().videos().list(id=self.id, part='snippet,statistics').execute()
        return video

    @property
    def like_count(self):
        """
        Показывает кол-во лайков
        """
        return self.channel_info["items"][0]["statistics"]["likeCount"]


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str) -> None:
        self.id = video_id
        self.playlist_id = playlist_id
        self.__title = super().title
        self.__url = super().url
        self.__view_count = super().view_count
        self.__like_count = super().like_count
