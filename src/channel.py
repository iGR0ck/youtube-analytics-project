from googleapiclient.discovery import build
import os
import json

# ключ для переменной окружения
YOUTUBE_API_KEY: str = os.getenv('YT_API_KEY')

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id


    def __str__(self):
        """
        Выводит название канала и ссылку на канал
        """
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        if type(other) == Channel:
            return self.subscriber_count + other.subscriber_count
        else:
            raise TypeError


    def __sub__(self, other):
        """
        Вычисляет разницу подписчиков каналов
        """
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        """
        Сравнение подписчиков через оператор "больше"
        """
        return self.subscriber_count > other.subscriber_count


    def __ge__(self, other):
        """
        Сравнение подписчиков через оператор "больше или равно"
        """
        return self.subscriber_count >= other.subscriber_count


    def __lt__(self, other):
        """
        Сравнение подписчиков через оператор "меньше"
        """
        return self.subscriber_count < other.subscriber_count


    def __le__(self, other):
        """
        Сравнение подписчиков через оператор "меньше или равно"
        """
        return self.subscriber_count <= other.subscriber_count


    def __eq__(self, other):
        """
        Приравнивание чисел подписчиков друг к другу через "="
        """
        return self.subscriber_count == other.subscriber_count


    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        # объект для работы с API
        cls.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        return cls.youtube

    @property
    def channel_info(self):
        """
        Возвращает информацию по каналу.
        """
        channel = Channel.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале в json."""
        info = json.dumps(self.channel_info, indent=2, ensure_ascii=False)
        return info

    # Атрибуты класса
    @property
    def title(self):
        return self.channel_info["items"][0]["snippet"]["title"]

    @property
    def description(self):
        return self.channel_info["items"][0]["snippet"]["description"]

    @property
    def url(self):
        return self.channel_info["items"][0]["snippet"]["thumbnails"]["default"]["url"]

    @property
    def subscriber_count(self):
        return self.channel_info["items"][0]["statistics"]["subscriberCount"]

    @property
    def video_count(self):
        return self.channel_info["items"][0]["statistics"]["videoCount"]

    @property
    def view_count(self):
        return self.channel_info["items"][0]["statistics"]["viewCount"]

    def to_json(self, json_file_name):
        """
        Сохраняет в файл значения атрибутов экземпляра Channel
        """
        examples = {'attribute': []}
        examples['attribute'].extend(
            [{'id': self.__channel_id, 'title': self.title, 'description': self.description, 'url': self.url,
              'subscriber_count': self.subscriber_count, 'video_count': self.video_count,
              'view_count': self.view_count}])
        with open(json_file_name, 'w') as file:
            json.dump(examples, file, indent=2, ensure_ascii=False)
