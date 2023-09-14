python -m pip install --user poetry==1.6.1
cd src
python -m poetry config virtualenvs.in-project true
python -m poetry install
