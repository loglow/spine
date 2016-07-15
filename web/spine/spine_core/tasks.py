from celery import shared_task
from .spider import ProjectTree
from .crawler import ProjectCrawler
from .models import File, Depend, Repo
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime


def add_or_get_file(path, repo):
    possibles = File.objects.filter(path=path)
    if not possibles:
        entry = File(
            path=path,
            repo=repo,
            last_version="90",
            last_edited = timezone.now())
        entry.save()
    else:
        entry = possibles[0]
    return entry


def add_or_get_deps(master, depend):
    possibles = Depend.objects.filter(master_file=master, depend_file=depend)
    if not possibles:
        entry = Depend(
            master_file=master,
            depend_file=depend,
            master_version=master.last_version,
            master_last_edited=master.last_edited,
            depend_version=depend.last_version,
            depend_last_edited=depend.last_edited)
        entry.save()
    else:
        entry = possibles[0]
    return entry


@shared_task
def list_current(repo_id):
    repo = get_object_or_404(Repo, pk=repo_id)
    spider = ProjectTree(repo.root_path)
    files = spider.all_files()
    for f in files:
        add_or_get_file(f, repo)


@shared_task
def dep_current(repo_id):
    repo = get_object_or_404(Repo, pk=repo_id)
    crawler = ProjectCrawler(repo.root_path)
    for mainfile, depfiles in crawler.check_project():
        main_db = add_or_get_file(mainfile, repo)
        for depfile in depfiles:
            dep_db = add_or_get_file(depfile, repo)
            add_or_get_deps(main_db, dep_db)
