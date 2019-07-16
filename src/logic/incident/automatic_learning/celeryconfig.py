from datetime import timedelta


CELERY_TIMEZONE = 'UTC'

CELERYBEAT_SCHEDULE = {
    'svm_classification-every-15-seconds': {
    'task': 'celery_learning_tasks.svm_classification',
    'schedule': timedelta(seconds=15),
    },
}