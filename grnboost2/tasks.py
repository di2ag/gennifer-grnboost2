import os
import time

from celery import Celery

from .gennifer_api import generateInputs, run, parseOutput

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
celery.conf.task_routes = {"create_grnboost2_task": {"queue": 'grnboost2'}}

@celery.task(name="create_grnboost2_task")
def create_grnboost2_task(zenodo_id):
    inputs = generateInputs(zenodo_id)
    res = run(inputs)
    output = parseOutput(res)
    return output
