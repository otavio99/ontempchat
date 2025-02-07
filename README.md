# Getting Started

- On another terminal, activate the env for the project `source .env/bin/activate` (in case you are using venv)
- Run `python main.py`
- Kill a process in port 5000 in case there is any executing (lots of utilities utilize port 5000):``` sudo kill -9 `sudo lsof -t -i:5000` ```
