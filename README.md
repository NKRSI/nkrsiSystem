## NKRSI system

### How to run?

Copy [configDefault.py](nkrsiSystem/configDefault.py) as [config.py](nkrsiSystem/config.py) and adjust to your settings.

#### Using docker

Run:
```shell
docker-compose -f docker-compose-dev.yml up --build -d
```

Docker image for your app should be built and postgres docker image should be pulled. Your app should be running at [127.0.0.1:8000](127.0.0.1:8000).

If postgres container wasn't created before (or if postgres volume was removed), it will have no users. To create superuser you can use the following:
```shell
docker exec -it nkrsisystem-nkrsi-system-1 bash
```
to start bash session inside the container. To create superuser use the following command:
```shell
python manage.py createsuperuser
```
You will be asked for email and password.

### Docker only for database

It is more convenient way of developing because after changing file at your PC webpage will be automatically refreshed.

Run:
```shell
docker-compose -f docker-postgres.yml up -d
```

To run app use the following command:
```shell
python ./manage.py migrate; python ./manage.py compilemessages -l pl; python ./manage.py runserver 0.0.0.0:8000;
```

Your app should be running at [127.0.0.1:8000](127.0.0.1:8000).

To create superuser you can use:
```shell
python manage.py createsuperuser
```
You will be asked for email and password.

