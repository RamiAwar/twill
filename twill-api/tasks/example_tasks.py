import app.service.data as data_service
from celery import BaseSingletonTask, app
from celery_config import CelerySettings


@app.task(
    base=BaseSingletonTask,
    lock_expiry=600,  # every 10 minutes
    time_limit=(500, 600),
    unique_on=["calibration_id"],
)
def fetch_recent_tweets(calibration_id: str):
    return data_service.process_calibration(calibration_id=calibration_id)


@app.task(base=BaseSingletonTask, lock_expiry=580)
def calibrate_all_pending():

    for calibration_id in ids:
        process_calibration.apply_async(
            {"calibration_id": calibration_id}, queue=CelerySettings.scheduling_queue
        )


def process_calibration(calibration_id: str):
    """Processes Calibrations"""
    return CalibrationService().process_calibration(calibration_id=calibration_id)
