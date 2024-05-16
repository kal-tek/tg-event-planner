#!/usr/bin/env bash

python ./manage.py migrate

if [ "$ENVIRONMENT" = "production" ]; then
	python ./manage.py collectstatic
	gunicorn \
		--bind 0.0.0.0:80 \
		--error-logfile '-' \
		--access-logfile '-' \
		--timeout 20 \
		--workers 2 \
		--threads 2 \
		event_planner.wsgi:application

elif [ "$ENVIRONMENT" = "staging" ]; then
	env DJANGO_SUPERUSER_PASSWORD=averystrongpasswordindeed \
		python ./manage.py createsuperuser --noinput \
		--email admin@flawlessworkflow.com \
		--username admin

	python ./manage.py collectstatic
	python ./manage.py loaddata initial_data
	gunicorn \
		--bind 0.0.0.0:80 \
		--error-logfile '-' \
		--access-logfile '-' \
		--timeout 20 \
		--workers 2 \
		--threads 2 \
		event_planner.wsgi:application

else
	env DJANGO_SUPERUSER_PASSWORD=admin python ./manage.py createsuperuser --email admin@example.com --first_name Admin --last_name User --noinput
	python ./manage.py loaddata initial_data
	python ./manage.py loaddata sample_data
	python ./manage.py runserver_plus 0.0.0.0:8000 --print-sql
fi
