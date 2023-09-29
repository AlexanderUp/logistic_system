from celery import shared_task

from tracks.utils import randomize_vehicle_positions


@shared_task
def randomize_vehicle_position_task():
    randomize_vehicle_positions()
