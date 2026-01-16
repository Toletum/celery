from celery import Celery

# Configure the Celery app
# 'tasks' is the name of the current module
# broker: where the messages are sent (Redis)
# backend: where the results are stored (Redis)
app = Celery(
    "my_project",
    broker="redis://redis-server:6379/0",
    backend="redis://redis-server:6379/0",
)

# Optional configuration
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

app.conf.worker_send_task_events = True
app.conf.task_send_sent_event = True
app.conf.task_track_started = True
app.conf.result_extended = True


@app.task
def add_numbers(x, y):
    """
    A simple task to demonstrate Celery functionality
    """
    return {"add": x + y}
