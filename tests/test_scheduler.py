
import unittest
from mongoengine import disconnect
from celerybeatmongo.schedulers import MongoScheduler
from celery import Celery


class MongoSchedulerTest(unittest.TestCase):

    def setUp(self):
        conf = {
            "mongodb_scheduler_url": "mongomock://localhost"
        }
        self.app = Celery(**conf)
        self.app.conf.update(**conf)
        self.scheduler = MongoScheduler(app=self.app)

    def tearDown(self):
        disconnect()

    def test_get_from_database(self):
        from celerybeatmongo.models import PeriodicTask
        PeriodicTask.objects.create(name="a1", task="foo", enabled=True, interval=PeriodicTask.Interval(every=1, period="days"))
        PeriodicTask.objects.create(name="b1", task="foo", enabled=True, interval=PeriodicTask.Interval(every=2, period="days"))
        PeriodicTask.objects.create(name="c2", task="foo", enabled=False, interval=PeriodicTask.Interval(every=3, period="days"))

        scheduler = MongoScheduler(app=self.app)
        self.assertEqual(2, len(scheduler.get_from_database())
                         , "get_from_database should return just enabled tasks")
