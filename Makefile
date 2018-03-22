deploy:
	rm -fr dist/ django_imagefit.egg-info/
	python setup.py sdist
	twine upload dist/*
