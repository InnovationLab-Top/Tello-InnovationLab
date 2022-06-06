virtualenv --python=python3 venv
activate () {
    . $PWD/venv/bin/activate
}
activate
pip install -r requirements.txt
pip install protobuf==3.20.*
