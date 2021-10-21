import shutil
from typing import IO, TextIO
import aiofiles.os
import ormar.exceptions
from moviepy.editor import *

import uvicorn

from db.base import database, metadata, engine



from fastapi import FastAPI, File, UploadFile, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from video.schemas import UploadVideo, GetVideo, Message, Text

from video.models import Video, Audio, VideoAudio
from video.service import save_video
from video.service import save_audiomp3
from video.service import save_audiowav
from video.service import save_videotoaudio
from pathlib import Path
from video.models import TextTransc
import os



app = FastAPI()


metadata.create_all(engine)
app.state.database = database



@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()





app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

'''--------------'''

@app.get('/forms', response_class=HTMLResponse)
def get_registration(request: Request):

    return templates.TemplateResponse('base_body_temp2.html', {'request': request})

'''-----------------Старт mp4
Загрузка видео файла - mpg4'''

@app.post("/videototext", response_model=Video, response_class=HTMLResponse)
async def upload_file_mp4(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...), file_text_ext: str = '1'):
    """ Add video """
    return await save_video(file, title, description, file_text_ext)

@app.get('/videototext', response_class=HTMLResponse)
def upload_file_mp4(request: Request):


    return templates.TemplateResponse('videototext.html', {'request': request})

# @app.get('/download{text_pk}', response_model=Video, response_class=HTMLResponse)
# async def text_transcr(file_text_ext: str) -> TextIO:
#     try:
#         file = Video.objects.get(file_text_ext=file_text_ext)
#     except ormar.exceptions.NoMatch:
#         raise HTTPException(status_code=404, detail="файл не найден")
#     path = Path(file.dict().get('file'))
#     file = path.open('r')
#     return file



''' Конец mp4'''

'''-------------Регистрация'''

@app.get('/registration', response_class=HTMLResponse)
def get_registration(request: Request):

    return templates.TemplateResponse('registration.html', {'request': request})

@app.get('/profile', response_class=HTMLResponse)
def get_profile(request: Request):


    return templates.TemplateResponse('profile.html', {'request': request})

@app.post('/info')
async def info_set(info: UploadVideo):
    return info


'''--------------------- Скачать файл'''

@app.get('/download', response_class=HTMLResponse)
def get_download(request: Request):


    return templates.TemplateResponse('download.html', {'request': request})

path = '/home/julia/dev/fastapi-audiototext/video/media/'


@app.get('/download_notfound')
async def download_txt():
    file_path = os.path.join(path, 'file_name.txt')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {'error': 'File not found'}

@app.get('/download_1', responses={200: {'description': 'Файл успешно получен'}})
async def getfiletext():
    file_path = os.path.join(path, 'file_name.txt')
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='multipart/form-data', filename='file_name.txt')
    return {'error': 'File not found'}

@app.get('/audio/{file_name}', response_model=Video, responses={404: {'model': Message}})
async def get_videov(file_name: str):
    return await Video.objects.get(pk=file_name)

'''-----------------
Микрофон'''

@app.get('/voicetotext', response_class=HTMLResponse)
def get_voicetotext(request: Request):


    return templates.TemplateResponse('voicetotext.html', {'request': request})




'''--------------Загрузка аудио файла- mp3'''

@app.post("/index", response_model=Audio, response_class=HTMLResponse)
async def upload_file_mp3(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    """ Add video """
    return await save_audiomp3(file, title, description)

@app.get('/index', response_class=HTMLResponse)
def upload_file_mp3(request: Request):


    return templates.TemplateResponse('index_.html', {'request': request})


'''-----------------Загрузка wav'''

@app.post("/audiototext", response_model=Audio, response_class=HTMLResponse)
async def upload_file_wav(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    """ Add video """
    return await save_audiowav(file, title, description)

@app.get('/audiototext', response_class=HTMLResponse)
def upload_file_wav(request: Request):


    return templates.TemplateResponse('audiototext.html', {'request': request})


'''Добавить слова в библиотеку'''

@app.get('/add_words', response_class=HTMLResponse)
def get_add_words(request: Request):


    return templates.TemplateResponse('add_words.html', {'request': request})



'''Забрать аудио из видео файла'''

@app.post("/videotoaudio", response_model=VideoAudio, response_class=HTMLResponse)
async def upload_file_mp3(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    """ Add video """
    return await save_videotoaudio(file, title, description)

@app.get('/videotoaudio', response_class=HTMLResponse)
def upload_file_mp3(request: Request):


    return templates.TemplateResponse('videotoaudio.html', {'request': request})



if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)






