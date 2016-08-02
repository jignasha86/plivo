APP_LIST ?= plivoapis

run:
	python manage.py runserver 0.0.0.0:8000

install:
	pip install -r requirements.txt

test:
	python manage.py test -v2 $(APP_LIST)

