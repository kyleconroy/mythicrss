.PHONY: test install deploy run teams stage


install: venv
	venv/bin/pip install -r requirements.txt

venv:
	virtualenv --python=python3.3 venv

serve: venv
	venv/bin/python mythicrss.py


test:
	venv/bin/flake8 tests mythicrss.py
	venv/bin/nosetests tests
