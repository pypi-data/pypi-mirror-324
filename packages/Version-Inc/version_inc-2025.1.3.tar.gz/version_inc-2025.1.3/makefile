py=.venv/bin/python
cli=vinc

build: .requirements
	make clean
	$(py) -m build

clean:
	touch dist/fuck
	rm dist/*

upload:
	vinc
	make build
	$(py) -m twine upload --repository pypi dist/* $(flags)

reload:
	make upload
	pipx upgrade $(cli)
	pipx upgrade $(cli)

.requirements:
	touch .requirements
	$(py) -m pip install build twine
