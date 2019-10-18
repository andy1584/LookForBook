from .celery import celery

@celery.task()                                             
def worker_task():                                                             
    return "Celery наконец-то заработала..."  

 