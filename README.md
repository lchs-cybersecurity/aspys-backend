⚙ Email Domain Verifier Extension Backend ⚙
===

Backend for the LCHS Cybersecurity Club's [Email Domain Verifier](https://github.com/lchs-cybersecurity/email-domain-verifier) web extension. Being written in Python, this *can* be run natively but in many cases would best be used with Docker.

Install/Run on Docker
---
1. Make sure [Docker is installed](https://docs.docker.com/install/).
2. `./build.sh && ./run.sh`

Install/Run on native \*nix
---
1. Make sure `python3` and `python3-pip` are installed.
2. `pip3 install requirements.txt`
3. /usr/bin/python3 main.py

Install/Run on native Windows
---
1. Make sure [Python 3.7.x for Windows](https://www.python.org/downloads/windows/) is installed.
2. `py.exe -3.7 -m pip install .\requirements.txt`
3. `py.exe -3.7 .\main.py`