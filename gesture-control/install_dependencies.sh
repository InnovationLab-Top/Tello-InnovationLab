virtualenv --python=python3 venv
activate () {
    . $PWD/venv/bin/activate
}
activate
pip install -r requirements.txt
