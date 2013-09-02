.PHONY: test install deploy run teams stage


install: venv
	venv/bin/pip install -r requirements.txt

venv:
	virtualenv --python=python3.3 venv

serve: venv
	venv/bin/python mythicrss/__init__.py


test:
	venv/bin/flake8 tests mythicrss
	venv/bin/nosetests tests
