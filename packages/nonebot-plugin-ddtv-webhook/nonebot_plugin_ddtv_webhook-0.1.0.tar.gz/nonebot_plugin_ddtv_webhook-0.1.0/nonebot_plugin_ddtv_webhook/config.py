from typing import Optional, List, Union
from pydantic import BaseModel


ID = Union[str, int]


class Config(BaseModel, extra="ignore"):
    ddtv_webhook_token: Optional[str] = None
    ddtv_webhook_send_to: Optional[List[ID]] = None
    ddtv_webhook_send_to_group: Optional[List[ID]] = None
    ddtv_webhook_route: str = "/ddtv_webhook"
    superusers: List[str]


class Title(BaseModel):
    Value: str


class RoomDescription(BaseModel):
    Value: str


class LiveTime(BaseModel):
    Value: int


class LiveStatus(BaseModel):
    Value: int


class ShortID(BaseModel):
    Value: int


class CoverFromUser(BaseModel):
    Value: str


class Keyframe(BaseModel):
    Value: str


class DownloadFileList(BaseModel):
    TranscodingCount: int
    VideoFile: List[str]
    DanmuFile: List[str]
    SCFile: List[str]
    GiftFile: List[str]
    GuardFile: List[str]
    CurrentOperationVideoFile: str
    SnapshotGenerationInProgress: bool


class DownInfo(BaseModel):
    LiveChatListener: List[str]
    IsDownload: bool
    IsCut: bool
    taskType: int
    DownloadSize: int
    RealTimeDownloadSpe: float
    Status: int
    StartTime: str
    EndTime: str
    DownloadFileList: DownloadFileList


class Data(BaseModel):
    Title: Title
    description: RoomDescription
    live_time: LiveTime
    live_status: LiveStatus
    live_status_end_event: bool
    short_id: ShortID
    cover_from_user: CoverFromUser
    keyframe: Keyframe
    CurrentMode: int
    DownInfo: DownInfo
    Name: str
    Description: str
    RoomId: int
    UID: int
    IsAutoRec: bool
    IsRemind: bool
    IsRecDanmu: bool
    Like: bool
    Shell: str
    AppointmentRecord: bool


class DdtvWebhookBody(BaseModel):
    cmd: str
    code: int
    data: Data
    message: str
