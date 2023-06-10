# docker-flask-microservice

A really simple microservice.

## Running the example

* Either with docker

```shell
docker build -t docker-flask-microservice:latest src
docker run -it -e PORT=5000 -p 5000:5000 docker-flask-microservice
docker push docker-flask-microservice:latest
```

* Or directly

```shell
pip install -r src/requirements.txt
pytest -v
python.exe src/run.py
```

## References

![linkedin](linkedin.png)