<div align="center">
    <img src="static/favicon.ico" height=100/><br>
<h1>⚙ Aspys Backend ⚙</h1>
</div>

Backend for the LCHS Cybersecurity Club's [Aspys](https://github.com/lchs-cybersecurity/aspys) extension.

# Installing and Running

First set the environment variables by renaming `example.env` to `.env` and populating the values or (recommended for production) setting the environment variables directly.

Install/Run on \*nix
---
1. Make sure `python3` and `python3-pip` are installed.
2. `pip3 install -r requirements.txt` OR use `pipenv shell` and `pipenv install`
3. `/usr/bin/python3 wsgi.py`

Install/Run on Windows
---
1. Make sure [Python 3.7.x](https://www.python.org/downloads/windows/) or 3.8.x is installed.
2. `py.exe -m pip install -r .\requirements.txt`
3. `py.exe .\wsgi.py`
