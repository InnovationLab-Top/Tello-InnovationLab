virtualenv --python=python3 venv
activate () {
    . $PWD/venv/bin/activate
}
activate
pip install cmake face_recognition opencv-python numpy mttkinter
sudo apt install -y libswscale-dev libavcodec-dev libavutil-dev libboost-all-dev python3-tk
sudo apt install -y python-imaging-tk
git clone https://github.com/DaWelter/h264decoder.git
cd h264decoder
pip install .
cd ..
rm -rf h264decoder
