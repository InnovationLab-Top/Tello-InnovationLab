virtualenv --python=python3 venv
activate () {
    . $PWD/venv/bin/activate
}
activate
pip install av==9.2.0
pip install numpy==1.22.3
pip install opencv-python==4.3.0.36
pip install opencv-contrib-python==4.3.0.36
pip install Pillow==9.1.0
pip install simple-pid==1.0.1
pip install tellopy
