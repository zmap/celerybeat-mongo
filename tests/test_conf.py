
import random
import unittest
import importlib

from celery import Celery
from mongoengine import disconnect


class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.app = Celery()
        disconnect()

    def tearDown(self):
        disconnect()

    def test_collection_name(self):
        config_old = {"CELERY_MONGODB_SCHEDULER_COLLECTION": "REC" + str(random.randint(10, 1000))}
        self.app.conf.update(**config_old)
        import celerybeatmongo
        importlib.reload(celerybeatmongo)
        self.assertEqual(celerybeatmongo.COLLECTION_NAME, config_old["CELERY_MONGODB_SCHEDULER_COLLECTION"])

        config_new = {"mongodb_scheduler_collection": "BAC" + str(random.randint(10, 1000))}
        self.app.conf.update(**config_new)
        importlib.reload(celerybeatmongo)
        self.assertEqual(celerybeatmongo.COLLECTION_NAME, config_new["mongodb_scheduler_collection"])

        self.app = Celery()
        importlib.reload(celerybeatmongo)
        self.assertEqual("schedules", celerybeatmongo.COLLECTION_NAME,
                         "The default value for scheduler collection is 'schedules'")

    def test_db_name(self):
        config_old = {"CELERY_MONGODB_SCHEDULER_DB": "DB" + str(random.randint(10, 1000))}
        self.app.conf.update(**config_old)
        import celerybeatmongo
        importlib.reload(celerybeatmongo)
        disconnect()
        self.assertEqual(celerybeatmongo.db, config_old["CELERY_MONGODB_SCHEDULER_DB"])

        config_new = {"mongodb_scheduler_db": "db" + str(random.randint(10, 1000))}
        self.app.conf.update(**config_new)
        importlib.reload(celerybeatmongo)
        disconnect()
        self.assertEqual(celerybeatmongo.db, config_new["mongodb_scheduler_db"])

        self.app = Celery()
        importlib.reload(celerybeatmongo)
        self.assertEqual("celery", celerybeatmongo.db, "The default value db name is 'celery'")

    def test_connection_alias(self):
        config_old = {"CELERY_MONGODB_SCHEDULER_CONNECTION_ALIAS": "ALIAS" + str(random.randint(10, 1000))}
        self.app.conf.update(**config_old)
        import celerybeatmongo
        importlib.reload(celerybeatmongo)
        disconnect()
        self.assertEqual(celerybeatmongo.alias, config_old["CELERY_MONGODB_SCHEDULER_CONNECTION_ALIAS"])

        config_new = {"mongodb_scheduler_connection_alias": "alias" + str(random.randint(10, 1000))}
        self.app.conf.update(**config_new)
        importlib.reload(celerybeatmongo)
        disconnect()
        self.assertEqual(celerybeatmongo.alias, config_new["mongodb_scheduler_connection_alias"])

        self.app = Celery()
        importlib.reload(celerybeatmongo)
        disconnect()
        self.assertEqual("default", celerybeatmongo.alias, "The default connection alias is 'default'")

    def test_connection_host(self):
        config_old = {"CELERY_MONGODB_SCHEDULER_URL": "ALIAS" + str(random.randint(10, 1000))}
        self.app.conf.update(**config_old)
        import celerybeatmongo
        importlib.reload(celerybeatmongo)
        disconnect()
        self.assertEqual(celerybeatmongo.host, config_old["CELERY_MONGODB_SCHEDULER_URL"])

        config_new = {"mongodb_scheduler_url": "alias" + str(random.randint(10, 1000))}
        self.app.conf.update(**config_new)
        importlib.reload(celerybeatmongo)
        disconnect()
        self.assertEqual(celerybeatmongo.host, config_new["mongodb_scheduler_url"])

        self.app = Celery()
        importlib.reload(celerybeatmongo)
        self.assertIsNone(celerybeatmongo.host)