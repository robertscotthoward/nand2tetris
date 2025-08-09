# Nand2Tetris Assembler

This code is basic Python 3 code. Should run in any environment. I use "uv" but you can pip install the few dependencies manually defined in the `pyproject.toml` file.

# Usage (Windows 11)
## First Time
* Ensure "[uv](https://docs.astral.sh/uv/)" is installed. If not, see below.
* Clone the repo.
* Run `reset-venv.bat`

## Thereafter
* Run `dev-cmd.bat`
* Run `python main.py`


## uv
If you want all your projects to be on D drive, then create environment variable: UV_CACHE_DIR=D:\uv
This makes all your projects on D drive use hard links for libraries, which is very fast.


Install `uv`, e.g. scoop, pip, pipx, etc. Verify with `uv --help`
