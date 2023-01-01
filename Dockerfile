FROM python:3.7

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update
RUN apt-get -y install gettext
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY ./static /static
EXPOSE 80 8080 4352

CMD bash -c "sleep 10; python ./manage.py migrate; python ./manage.py compilemessages -l pl; python ./manage.py runserver 0.0.0.0:80;"
