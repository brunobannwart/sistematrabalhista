FROM tiangolo/uwsgi-nginx:python3.8

COPY django_requirements.txt /app
# install the requirments
RUN pip3 install -r /app/django_requirements.txt
