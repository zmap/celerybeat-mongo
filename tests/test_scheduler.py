
import unittest
from mongoengine import disconnect
from celery import Celery


class MongoSchedulerTest(unittest.TestCase):

    def setUp(self):
        conf = {
            "mongodb_scheduler_url": "mongomock://localhost"
        }
        self.app = Celery(**conf)
        self.app.conf.update(**conf)

    def tearDown(self):
        disconnect()

    def test_all_as_schedule(self):
        from celerybeatmongo.schedulers import MongoScheduler
        from celerybeatmongo.models import PeriodicTask, Interval
        PeriodicTask.drop_collection()

        PeriodicTask.objects.create(name="a1", task="foo", enabled=True, interval=Interval(every=1, period="days"))
        PeriodicTask.objects.create(name="b1", task="foo", enabled=True, interval=Interval(every=2, period="days"))
        PeriodicTask.objects.create(name="c2", task="foo", enabled=False, interval=PeriodicTask.Interval(every=3, period="days"))

        scheduler = MongoScheduler(app=self.app)
        self.assertEqual(2, len(scheduler.all_as_schedule())
                         , "all_as_schedule should return just enabled tasks")