from googleapiclient.discovery import build
import os
import json

class Channel:
    """Класс для ютуб-канала"""

    # ключ для переменной окружения
    api_key: str = os.getenv('YT_API_KEY')

    # объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        info = json.dumps(channel, indent=2, ensure_ascii=False)
        print (info)
