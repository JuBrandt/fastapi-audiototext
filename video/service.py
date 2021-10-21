import asyncio
import shutil
import ormar
from math import *
import subprocess
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import aiofiles, aiofiles.os
import pyaudio



from os.path import join
from uuid import uuid4
from moviepy.editor import *
from fastapi import UploadFile, HTTPException


from .models import Video, VideoAudio, Audio, TextTransc
from .schemas import UploadVideo, UploadVideoAudio, UploadAudio

'''Обрабатываем MP4.

Функция проверяет формат файла. Должен быть видео файл mp4. Если все верно - вызывает функцию write_vdeo'''

async def save_video(
        file: UploadFile,
        title: str,
        description: str,
        file_text_ext: str


):

    file_name = f'{uuid4()}_{file.filename}'
    if file.content_type == 'video/mp4':

        await write_video(file_name, file, file_text_ext)
    else:
        raise HTTPException(status_code=418,
                            detail="Это не mp4 формат. Проверьте файл.")
    info = UploadVideo(title=title, description=description)
    return await Video.objects.create(file=file_name, **info.dict(), file_text_ext=file_text_ext)


'''Функция проверяет размер файла. Размер можно регулировать. 
https://www.dmosk.ru/instruktions.php?object=kbites#converter
 Установлено в байтах. Значение установлено до 300 Мб. 
Если все верно. Файл сохраняется. Дальше вызывается программа обработки звука в текст.'''

async def write_video(file_name: str, file: UploadFile, file_text_ext: str):
    async with aiofiles.open(file_name, "wb") as buffer:
        for i in range(10):
            data = await file.read()
            await buffer.write(data)
    async with aiofiles.open(file_name, mode='r'):
        file_stat = await aiofiles.os.stat(file_name)
        if file_stat.st_size <= 314572800:

            await run_threads(file_name, file, file_text_ext)

        else:
            await aiofiles.os.remove(file_name)
            raise HTTPException(status_code=418,
                                    detail="Проверьте размер файла. Должен быть не больше 300 mb")




'''Вызывается программа обработки звука в текст'''

async def run_threads(file_name: str, file: UploadFile, file_text_ext: str):
    with open(f'{file_name}', 'rb'):
        with open(f'{file_name}.txt', 'w'):

            cmd = f"python3 test_ffmpeg_ru.py {file_name}"
            p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, text=True,
                                  )
            out = p1.communicate()
            file_text = shutil.copy2(r'file_name.txt', f'{file_name}.txt')
            print(out)
            print(file_text_ext)

    return run_threads(file_name, file, file_text_ext=file_text)




'''-----------Загрузка аудио mp3. Функция проверяет формат файла. 
Должен быть видео файл mp4. Если все верно - вызывает функцию write_vdeo'''

async def save_audiomp3(
        file: UploadFile,
        title: str,
        description: str,

):
    file_name = f'{uuid4()}_{file.filename}'
    if file.content_type == 'media/mp3':
        await write_audiomp3(file_name, file)
    else:
        raise HTTPException(status_code=418,
                            detail="Это не mp4 формат. Проверьте файл.")
    info = UploadAudio(title=title, description=description)
    return await Audio.objects.create(file=file_name, **info.dict())


'''Функция проверяет размер файла. Размер можно регулировать. 
https://www.dmosk.ru/instruktions.php?object=kbites#converter
 Установлено в байтах. Значение установлено до 300 Мб. 
Если все верно. Файл сохраняется. Дальше вызывается программа обработки звука в текст.'''

async def write_audiomp3(file_name: str, file: UploadFile):
    async with aiofiles.open(file_name, "wb") as buffer:
        for i in range(10):
            data = await file.read()
            await buffer.write(data)
    async with aiofiles.open(file_name, mode='r'):
        file_stat = await aiofiles.os.stat(file_name)
        if file_stat.st_size <= 314572800:

            await run_threadsmp3(file_name, file)

        else:
            await aiofiles.os.remove(file_name)
            raise HTTPException(status_code=418,
                                    detail="Проверьте размер файла. Должен быть не больше 300 mb")




'''Вызывается программа обработки звука в текст'''

async def run_threadsmp3(file_name: str, file: UploadFile, file_text_ext: str):
    with open(f'{file_name}', 'rb'):
        with open(f'{file_name}.txt', 'w'):

            cmd = f"python3 test_ffmpeg_ru.py {file_name}"
            p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, text=True,
                                  )
            out = p1.communicate()
            file_text = shutil.copy2(r'file_name.txt', f'{file_name}.txt')
            print(out)
            print(file_text_ext)
    return run_threadsmp3(file_name, file, file_text_ext=file_text)





'''-----------Загрузка аудио wav. Функция проверяет формат файла. Должен быть видео файл mp4. 
Если все верно - вызывает функцию write_vdeo'''

async def save_audiowav(
        file: UploadFile,
        title: str,
        description: str,

):
    file_name = f'{uuid4()}_{file.filename}'
    if file.content_type == 'video/mp4':
        await write_audiowav(file_name, file)
    else:
        raise HTTPException(status_code=418,
                            detail="Это не mp4 формат. Проверьте файл.")
    info = UploadAudio(title=title, description=description)
    return await Audio.objects.create(file=file_name, **info.dict())


'''Функция проверяет размер файла. Размер можно регулировать. 
https://www.dmosk.ru/instruktions.php?object=kbites#converter
 Установлено в байтах. Значение установлено до 300 Мб. 
Если все верно. Файл сохраняется. Дальше вызывается программа обработки звука в текст.'''

async def write_audiowav(file_name: str, file: UploadFile):
    async with aiofiles.open(file_name, "wb") as buffer:
        for i in range(10):
            data = await file.read()
            await buffer.write(data)
    async with aiofiles.open(file_name, mode='r'):
        file_stat = await aiofiles.os.stat(file_name)
        if file_stat.st_size <= 314572800:

            await run_threadswav(file_name, file)

        else:
            await aiofiles.os.remove(file_name)
            raise HTTPException(status_code=418,
                                    detail="Проверьте размер файла. Должен быть не больше 300 mb")




'''Вызывается программа обработки звука в текст'''

async def run_threadswav(file_name: str, file: UploadFile, file_text_ext: str):
    with open(f'{file_name}', 'rb'):
        with open(f'{file_name}.txt', 'w'):

            cmd = f"python3 test_ffmpeg_ru.py {file_name}"
            p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, text=True,
                                  )
            out = p1.communicate()
            file_text = shutil.copy2(r'file_name.txt', f'{file_name}.txt')
            print(out)
            print(type(file_text_ext))
    return run_threadswav(file_name, file, file_text_ext=file_text)



'''
-----------------Забрать аудио из видео'''


async def save_videotoaudio(
        file: UploadFile,
        title: str,
        description: str,

):
    file_name = f'{uuid4()}_{file.filename}'
    if file.content_type == 'video/mp4':
        await write_videotoaudio(file_name, file)
    else:
        raise HTTPException(status_code=418,
                            detail="Это не mp4 формат. Проверьте файл.")
    info = UploadVideoAudio(title=title, description=description)
    return await VideoAudio.objects.create(file=file_name, **info.dict())


'''Функция проверяет размер файла. Размер можно регулировать. 
https://www.dmosk.ru/instruktions.php?object=kbites#converter
 Установлено в байтах. Значение установлено до 300 Мб. 
Если все верно. Файл сохраняется. Дальше вызывается программа обработки звука в текст.'''

async def write_videotoaudio(file_name: str, file: UploadFile, file_audio_ext: str):
    async with aiofiles.open(file_name, "wb") as buffer:
        for i in range(10):
            data = await file.read()
            await buffer.write(data)
    async with aiofiles.open(file_name, mode='r'):
        file_stat = await aiofiles.os.stat(file_name)
        if file_stat.st_size <= 314572800:
            async with aiofiles.open(f'{file_name}.mp4', 'wb'):
                audioclip = AudioFileClip(f'{file_name}')
                file_audio = audioclip.write_audiofile(f'{file_name}.wav', fps=44100, buffersize=50000, codec='mp3', write_logfile=True, logger='bar')
                audioclip.close()
                print(file_audio_ext)

            return write_videotoaudio(file_name, file, file_audio_ext=file_audio)

        else:
            await aiofiles.os.remove(file_name)
            raise HTTPException(status_code=418,
                                    detail="Проверьте размер файла. Должен быть не больше 300 mb")


'''-------------------'''

def fake_video_streamer():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    if sys.platform == 'darwin':
        CHANNELS = 1

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=14,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return wf








