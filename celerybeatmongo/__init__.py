
from celery import current_app
from mongoengine import connect
from celery.utils.log import get_logger

logger = get_logger(__name__)

COLLECTION_NAME = None

if hasattr(current_app.conf, "mongodb_scheduler_collection"):
    COLLECTION_NAME = current_app.conf.get("mongodb_scheduler_collection")
elif hasattr(current_app.conf, "CELERY_MONGODB_SCHEDULER_COLLECTION"):
    COLLECTION_NAME = current_app.conf.get("CELERY_MONGODB_SCHEDULER_COLLECTION")
if not COLLECTION_NAME:
    COLLECTION_NAME = "schedules"

if hasattr(current_app.conf, "mongodb_scheduler_db"):
    db = current_app.conf.get("mongodb_scheduler_db")
elif hasattr(current_app.conf, "CELERY_MONGODB_SCHEDULER_DB"):
    db = current_app.conf.CELERY_MONGODB_SCHEDULER_DB
else:
    db = "celery"

if hasattr(current_app.conf, "mongodb_scheduler_connection_alias"):
    alias = current_app.conf.get('mongodb_scheduler_connection_alias')
elif hasattr(current_app.conf, "CELERY_MONGODB_SCHEDULER_CONNECTION_ALIAS"):
    alias = current_app.conf.CELERY_MONGODB_SCHEDULER_CONNECTION_ALIAS
else:
    alias = "default"

if hasattr(current_app.conf, "mongodb_scheduler_url"):
    host = current_app.conf.get('mongodb_scheduler_url')
elif hasattr(current_app.conf, "CELERY_MONGODB_SCHEDULER_URL"):
    host = current_app.conf.CELERY_MONGODB_SCHEDULER_URL
else:
    host = None

connection = connect(db, host=host, alias=alias)
