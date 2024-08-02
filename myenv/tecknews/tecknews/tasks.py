from .celery import app
from time import sleep


@app.task(name="SimpleTask1", queue="queue1")
def simple_task_1() -> None:
    for i in range(10):
        sleep(0.5)
        print(f"Simple Task 1: {i}")





