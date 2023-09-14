import os
from googleapiclient.discovery import build
from datetime import timedelta
import isodate


class PlayList:
    def __init__(self, playlist_id):
        """Инициализируем класс по id видео, также инициализируем
        название, количество просмотров и лайков"""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist_id = playlist_id
        self.playlist = youtube.playlists().list(id=playlist_id, part='snippet').execute()
        self.playlist_video = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails,snippet',
                                                           maxResults=50,).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_video['items']]
        self.videos = youtube.videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        duration_ = timedelta()
        total_duration_ = timedelta()
        for i in range(len(self.videos)):
            iso_8601_duration = self.videos['items'][i]['contentDetails']['duration']
            duration_ = isodate.parse_duration(iso_8601_duration)
            total_duration_ += duration_
        return total_duration_

    def total_seconds(self):
        return self.total_duration.seconds

    def show_best_video(self):
        videos = {}
        id_ = None
        likes = 0
        for i in range(len(self.playlist_video)):
            videos[self.videos['items'][i]['statistics']['likeCount']] = self.playlist_video['items'][i]
            if likes < int(self.videos['items'][i]['statistics']['likeCount']):
                likes = int(self.videos['items'][i]['statistics']['likeCount'])
                id_ = self.videos['items'][i]['id']
        return f"https://youtu.be/{id_}"
