clean:
	rm -f -r build/
	rm -f -r dist/
	rm -f -r *.egg-info
	rm -f -r __pycache__/
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +

publish: clean
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*

testpublish: clean
	python setup.py sdist bdist_wheel
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

rebuild: clean
	python setup.py install

build: clean
	python setup.py install

install: build

test:
	python3.7 setup.py test
