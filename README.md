## Dockerizing Flask With Compose and Machine - From Localhost to the Cloud

Featuring:

- Docker v1.10.3, build d12ea79c9de6d144ce6bc7ccfe41c507cca6fd35
- Docker Compose v1.6.2
- Docker Machine v0.6.0


**Check out the awesome blog post here > https://realpython.com/blog/python/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/**

## How to run


```
#!bash
docker compose up -d
```
```
#!bash
<vm_ip>:80 - d2rq-mapper
<vm_ip>:8080 - application
<vm_ip>:2021 - sparql endpoint
<vm_ip>:5432 - postgresql database
```