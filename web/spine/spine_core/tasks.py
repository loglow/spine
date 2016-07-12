from celery import shared_task
from .spider import ProjectTree

@shared_task
def list_current(project):
    return [i for i in project.all_files()]
