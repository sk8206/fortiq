"""Celery application configuration."""

import platform

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "fortiq",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.classify_task", "app.tasks.migrate_task"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,  # at-least-once delivery
    worker_prefetch_multiplier=1,  # process one task at a time
    task_soft_time_limit=600,  # 10-minute soft timeout
    task_time_limit=660,  # 11-minute hard kill
    task_default_queue="fortiq",
)

# Use solo pool on macOS to avoid fork() crashes with NumPy/PennyLane
# The prefork pool causes SIGABRT due to Objective-C runtime issues
if platform.system() == "Darwin":
    celery_app.conf.update(
        worker_pool="solo",
    )
