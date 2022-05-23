virtualenv --python=python3 venv
activate () {
    . $PWD/venv/bin/activate
}
activate
pip install deeppavlov
python -m deeppavlov install asr_tts
python -m deeppavlov download asr_tts
pip install python-levenshtein sounddevice torchaudio
pip install cmake
git clone https://github.com/DaWelter/h264decoder
cd h264decoder/
sudo apt install libswscale-dev libavcodec-dev libavutil-dev
pip install .
cd ..
rm -rf h264decoder
pip install torchaudio
pip install --upgrade torch torchvision
pip install pygame
