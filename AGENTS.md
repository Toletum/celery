# celery

Ejemplo de Celery con Redis como broker y backend de resultados, con Flower y Celery Insights para monitorizar, desplegado con Docker/Podman Compose.

## Visibilidad y rama
- Público (github.com/Toletum/celery). Rama por defecto: `main`.
- Descripción en GitHub: "Celery con Redis como broker".

## Stack
- Python (imagen `python:3.14-alpine`), Celery con extra `redis`.
- Redis (`redis:alpine`), Flower, `redis/redisinsight`, `ghcr.io/danyi1212/celery-insights`.
- No hay `requirements.txt`: la dependencia se instala a mano (`pip install "celery[redis]"`, según README).

## Estructura
- `mycelery.py`: app Celery (`my_project`), broker y backend `redis://redis-server:6379/0`, serialización JSON, y la tarea `add_numbers(x, y)`.
- `addjob.py`: encola `add_numbers.delay(10, 25)` y espera el resultado con `ready()` / `get()`.
- `docker-compose.yaml`: servicios `redis-server`, `redis-insight` (:5540), `celery` (worker), `flower` (:5555), `celery-insights` (:8555). El volumen `python` es externo.
- `README.md`: comandos para crear el volumen `python` y el entorno.

## Comandos
Preparación (según README, con Podman):
```bash
podman volume create python
podman run -ti --rm --name python --network celery_thenetwork -v python:/app python:3.14-alpine sh
source /app/venv/bin/activate
pip install "celery[redis]"
```
- El README no crea el venv (`python -m venv /app/venv`); no verificado si falta un paso.
- Arranque de servicios: `docker compose up` o `podman compose up` (no verificado).
- Worker: `celery -A mycelery worker --loglevel=info -E`. Flower: `celery -A mycelery flower`.
- Encolar: `python addjob.py` (dentro del contenedor, con `mycelery.py` en `/app`).
- Tests y lint: no hay.

## Configuración
- Sin variables de entorno. Las URLs de Redis están fijas en `mycelery.py` (`redis-server:6379/0`) y en `docker-compose.yaml`.
- Requiere el volumen externo `python` (`external: true`) creado antes, con `/app/venv` y el código.
- La red del compose se llama `thenetwork`; el README usa `celery_thenetwork`, que depende del nombre del proyecto Compose (directorio `celery`).

## Convenciones y reglas para agentes
- Tareas con `@app.task` en `mycelery.py`; devolver tipos serializables en JSON.
- El código no se monta en los servicios: el volumen `python` debe contener la versión actual de `mycelery.py`. Tras cambiar código, copiarlo al volumen.

## Estado
- Sin tests.
- `docker-compose.yaml` declara `version: "3.8"`, campo obsoleto en Compose v2.
- Worker y Flower dependen de `/app/venv` ya existente en el volumen: sin ese volumen no arrancan.
- Hosts y puertos fijos; no hay configuración por entorno.
- `addjob.py` hace polling cada segundo sin tiempo máximo.
