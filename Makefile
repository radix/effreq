lint:
	flake8 --ignore=E131 effreq/ examples/

build-dist:
	rm -rf dist
	python setup.py sdist bdist_wheel

upload-dist:
	twine upload dist/*
