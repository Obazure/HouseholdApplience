# Config for dev env
python -m venv backend/env
./backend/env/Scripts/python -m pip install -r backend/requirements.txt

cd frontend && npm install
