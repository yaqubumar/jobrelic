from celery import shared_task

from apps.profiles.api import _get_or_create_demo_profile

from .services import queue_auto_applications


@shared_task
def run_auto_apply_cycle() -> int:
    profile = _get_or_create_demo_profile()
    return queue_auto_applications(profile)
