import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = self.get_info().get('items')[0].get('snippet').get('title')
        self.description = self.get_info().get('items')[0].get('snippet').get('description')
        self.url = f"http://www.youtube.com/channel/{self.get_info().get('items')[0].get('id')}"
        self.subscriber_count = self.get_subscriber_count()
        self.video_count = self.get_info().get('items')[0].get('statistics').get('videoCount')
        self.viewCount = self.get_info().get('items')[0].get('statistics').get('viewCount')

    def get_subscriber_count(self):
        return int(self.get_info().get('items')[0].get('statistics').get('subscriberCount'))

    def __add__(self, other):
        return self.get_subscriber_count() + other.get_subscriber_count()

    def __sub__(self, other):
        return self.get_subscriber_count() - other.get_subscriber_count()

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __gt__(self, other):
        return  self.get_subscriber_count() > other.get_subscriber_count()

    def __ge__(self, other):
        return self.get_subscriber_count() >= other.get_subscriber_count()

    def __eq__(self, other):
        return self.get_subscriber_count() == other.get_subscriber_count()

    def __le__(self, other):
        return self.get_subscriber_count() <= other.get_subscriber_count()

    def __lt__(self, other):
        return self.get_subscriber_count() < other.get_subscriber_count()

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def chanel_id(self, channel_id):
        self.__channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def get_info(self):
        channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel

    def to_json(self, title):
        """Запись полученной информации с сайта в файл"""
        with open(title, 'w') as f:
            json.dump(self.get_info(), f, indent=3)

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

