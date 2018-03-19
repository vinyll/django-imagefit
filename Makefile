deploy:
  python setup.py register
  python setup.py sdist
  wine upload dist/*
