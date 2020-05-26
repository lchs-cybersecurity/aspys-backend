<div align="center">
    <img src="static/favicon.ico" height=100/><br>
<h1>⚙ Veritas Backend ⚙</h1>
</div>

Backend for the LCHS Cybersecurity Club's [Veritas](https://github.com/lchs-cybersecurity/email-domain-verifier) extension. Being written in Python, this can be run natively but in many cases would best be used with Docker.

# Installing and Running

First set the environment variables by renaming `example.env` to `.env` and populating the values or (recommended for production) setting the environment variables directly.

Install/Run on Docker
---
1. Make sure [Docker is installed](https://docs.docker.com/install/).
2. `./build.sh && ./run.sh`

Install/Run on native \*nix
---
1. Make sure `python3` and `python3-pip` are installed.
2. `pip3 install -r requirements.txt` or use `pipenv shell` and `pipenv install`
3. `/usr/bin/python3 wsgi.py`

Install/Run on native Windows
---
1. Make sure [Python 3.7.x](https://www.python.org/downloads/windows/) is installed.
2. `py.exe -3.7 -m pip install -r .\requirements.txt`
3. `py.exe -3.7 .\wsgi.py`
