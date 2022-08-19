from pydantic import BaseSettings, Field


class CelerySettings(BaseSettings):
    broker_url: str = Field(env="CELERY_BROKER_URL", default="redis://localhost:6379")
    backend_url: str = Field(env="CELERY_BACKEND_URL", default="redis://localhost:6379")

    example_schedule: int = Field(
        env="EXAMPLE_SCHEDULE", default=60 * 60 * 3
    )  # 3 hours
    scheduling_queue: str = Field(env="SCHEDULING_QUEUE", default="scheduling")


celery_settings = CelerySettings()


class CeleryConfig:
    broker_url = celery_settings.broker_url

    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]

    enable_utc = True

    task_store_errors_even_if_ignored = True

    beat_schedule = {
        "glucose_fetcher": {
            "task": "tasks.example_tasks",
            "schedule": celery_settings.example_schedule,
            "options": {"queue": celery_settings.scheduling_queue},
        }
    }
