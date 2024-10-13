from datetime import datetime
from functools import cached_property
from pandas import DataFrame
import os
from youtube_api import YouTubeDataAPI
from pydantic import BaseModel, PrivateAttr, RootModel


class ResponseChannelMetadata(BaseModel):
    playlist_id_uploads: str


class ResponseListVideos(BaseModel):
    video_id: str


class VideoMetadata(BaseModel):
    video_id: str
    channel_title: str
    video_publish_date: datetime
    video_title: str
    video_view_count: int
    video_comment_count: int
    video_like_count: int
    video_dislike_count: int | None


Videos = RootModel[list[VideoMetadata]]


class Channel(BaseModel):
    channel_id: str

    _yt: YouTubeDataAPI = PrivateAttr(YouTubeDataAPI(key=os.environ["YT_API_KEY"]))

    def to_dataframe(self) -> DataFrame:
        return DataFrame([video.model_dump() for video in self.uploaded_videos.root])

    @cached_property
    def uploaded_videos(self) -> Videos:
        return Videos.model_validate([self._yt.get_video_metadata(video.video_id) for video in self._uploaded_videos_metadata])

    @cached_property
    def _uploaded_videos_metadata(self) -> list[ResponseListVideos]:
        return [ResponseListVideos.model_validate(item) for item in self._yt.get_videos_from_playlist_id(self._metadata.playlist_id_uploads)]

    @cached_property
    def _metadata(self) -> ResponseChannelMetadata:
        return ResponseChannelMetadata.model_validate(self._yt.get_channel_metadata(self.channel_id))


def download_data():
    # used just once
    steve_mould = Channel(channel_id="UCEIwxahdLz7bap-VDs9h35A")
    real_engineering = Channel(channel_id="UCR1IuLEqb6UEA_zQ81kwXfg")

    steve_mould.to_dataframe().to_csv("steve.csv", index=False)
    real_engineering.to_dataframe().to_csv("real.csv", index=False)


if __name__ == "__main__":
    download_data()
