# a bunch of useful bash command to deal with virtual environments

```bash

# create a new venv:
python3 -m venv <venv-name>

# activate/deactivate the new venv
source ./<venv-name>/bin/activate
deactivate

# save all pip installed python deps
pip freeze > requirements.txt

# load all pip deps
pip install -r requirements.txt
