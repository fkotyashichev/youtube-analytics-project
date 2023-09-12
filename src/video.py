import os
from googleapiclient.discovery import build


class Video:

    def __init__(self, video):
        """Инициализируем класс по id видео, также инициализируем
        название, количество просмотров и лайков"""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.video = youtube.videos().list(id=video, part='snippet,contentDetails,statistics').execute()
        self.video_id = self.video["items"][0]["id"]
        self.video_title = self.video["items"][0]["snippet"]["title"]
        self.video_description = self.video["items"][0]["snippet"]["description"]
        self.video_views = self.video["items"][0]["statistics"]["viewCount"]
        self.video_likes = self.video["items"][0]["statistics"]["likeCount"]

    def __repr__(self):
        return self.video_title
