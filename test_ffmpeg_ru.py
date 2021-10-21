#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json
import subprocess
# from video.service.write_video import file_download


SetLogLevel(0)

if not os.path.exists("model/vosk-model-small-ru-0.15/"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

sample_rate=16000
model = Model("model/vosk-model-small-ru-0.15/")
rec = KaldiRecognizer(model, sample_rate)

process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                            sys.argv[1],
                            '-ar', str(sample_rate), '-ac', '1', '-f', 's16le', '-'],
                            stdout=subprocess.PIPE)
with open(f'file_name.txt', 'w', encoding='utf-8') as filess:
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            rec_text = json.loads(rec.Result())
            print(rec.Result())
            filess.writelines(f'{rec_text.get("text")}\n')
        else:
            print(rec.PartialResult())

    # filessin = rec.FinalResult()
    print(rec.FinalResult())


