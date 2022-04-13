.PHONY: test setup-environment

test:
	pytest test/

setup-environment:
	rm -rf env || true
	python3 -m venv env
	. ./env/bin/activate && pip3 install -r app/requirements.txt