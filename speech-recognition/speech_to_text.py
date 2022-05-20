from io import BytesIO

import sounddevice as sd
from scipy.io.wavfile import write

from deeppavlov import build_model, configs

def speech_to_text():
    sr = 16000
    duration = 3

    print('Recording...')
    myrecording = sd.rec(duration*sr, samplerate=sr, channels=1)
    sd.wait()
    print('done')

    out = BytesIO()
    write(out, sr, myrecording)

    model = build_model(configs.nemo.asr)
    text_batch = model([out])

    return text_batch[0]