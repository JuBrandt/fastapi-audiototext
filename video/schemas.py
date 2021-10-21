from pydantic import BaseModel





class UploadVideo(BaseModel):
    title: str
    description: str
    file_text_ext: str


class Text(BaseModel):
    file_text_ext: str



class GetVideo(BaseModel):

    video: UploadVideo



class Message(BaseModel):
    message: str


class UploadAudio(BaseModel):
    title: str
    description: str

class GetAudio(BaseModel):

    video: UploadAudio

class UploadVideoAudio(BaseModel):
    title: str
    description: str

class GetVideoAudio(BaseModel):

    video: UploadVideoAudio