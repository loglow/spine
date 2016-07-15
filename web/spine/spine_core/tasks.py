from celery import shared_task
from .spider import ProjectTree
from .crawler import ProjectCrawler
from .models import File, Depend, Repo
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime

@shared_task
def list_current(repo_id):
    print(repo_id)
    repo = get_object_or_404(Repo, repo_id)
    spider = ProjectTree("/home/bassam/projects/hamp/tube")
    files = spider.all_files()
    for f in files:
        entry = File(
            path=f,
            repo=repo.objects.all()[0],
            last_version="80",
            last_edited = timezone.now())
        entry.save()


@shared_task
def dep_current(rep_id):
    print(repo_id)
    repo = get_object_or_404(Repo, pk=repo_id)

