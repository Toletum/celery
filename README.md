```
podman volume create python
podman run -ti --rm --name python --network celery_thenetwork -v python:/app python:3.14-alpine sh
source /app/venv/bin/activate

pip install "celery[redis]"

```

```
podman run -ti --rm --name python --network celery_thenetwork -v python:/app python:3.14-alpine sh
source /app/venv/bin/activate
```
