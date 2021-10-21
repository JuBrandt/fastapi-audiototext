#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json


async def transcrib_fileru(file_name: str):
    SetLogLevel(0)

    if not os.path.exists("model/vosk-model-small-ru-0.15/"):
        print(
            "Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

    wf = wave.open(f'{file_name}', "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        exit(1)

    model = Model("model/vosk-model-small-ru-0.15/")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetMaxAlternatives(10)
    rec.SetWords(True)

    with open(f'{file_name}.txt', 'w', encoding='utf-8') as filess:
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                rec_text = json.loads(rec.Result())
                filess.writelines(f'{rec_text.get("text")}\n')
                print(json.loads(rec.Result()))
            else:
                print(json.loads(rec.PartialResult()))

        print(json.loads(rec.FinalResult()))





