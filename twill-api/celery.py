from celery_singleton import Singleton

from app.config import logger
from celery import Celery
from celery_config import CeleryConfig

app = Celery("twill-tasks", include=[])
app.config_from_object(CeleryConfig)


class BaseSingletonTask(Singleton):
    # This means the task may be executed multiple times should the
    # worker crash in the middle of execution. Make sure your tasks are idempotent.
    acks_late = True
    abstract = True
    auto_retry = Exception
    max_retries = 3
    default_retry_delay = 10
    ignore_result = True
    raise_on_duplicate = False

    def __call__(self, *args, **kwargs):
        logger.info(f"Task {self.name}: {args}, {kwargs}")
        self.run(*args, **kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"{self.name}: {task_id} failed: \n{exc}")
