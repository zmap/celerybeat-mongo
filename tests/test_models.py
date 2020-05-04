
import importlib
import unittest
from mongoengine import ValidationError
from celery import Celery

from celerybeatmongo.models import PeriodicTask
from tests import BeatMongoCase


class IntervalScheduleTest(BeatMongoCase):

    def test_cannot_save_interval_schduler_with_a_invalid_period(self):
        periodic = PeriodicTask(task="foo")
        with self.assertRaises(ValidationError):
            periodic.interval = PeriodicTask.Interval(every=1, period="days111")
            periodic.save()

    def test_scheduler(self):
        periodic = PeriodicTask(task="foo")
        periodic.interval = PeriodicTask.Interval(every=1, period="days")
        periodic.save()
        self.assertIsNotNone(periodic.schedule)

    def test_str(self):
        periodic = PeriodicTask(task="foo")
        periodic.interval = PeriodicTask.Interval(every=1, period="days")
        self.assertEqual("every day", str(periodic.interval))

        periodic.interval = PeriodicTask.Interval(every=2, period="days")
        self.assertEqual('every 2 days', str(periodic.interval))


class CrontabScheduleTest(unittest.TestCase):

    def test_str(self):
        periodic = PeriodicTask(task="foo")
        periodic.crontab = PeriodicTask.Crontab(minute="0", hour="*", day_of_week="*",
                                                day_of_month="10-15", month_of_year="*")
        self.assertEqual("0 * * 10-15 * (m/h/d/dM/MY)", str(periodic.crontab))


class PeriodicTaskTest(unittest.TestCase):

    def test_must_define_interval_or_crontab(self):
        with self.assertRaises(ValidationError) as err:
            periodic = PeriodicTask(task="foo")
            periodic.save()
        self.assertTrue("Must defined either interval or crontab schedule." in err.exception.message)

    def test_cannot_define_both_interval_and_contrab(self):
        periodic = PeriodicTask(task="foo")
        periodic.interval = PeriodicTask.Interval(every=1, period="days")
        periodic.crontab = PeriodicTask.Crontab(minute="0", hour="*", day_of_week="*",
                                                day_of_month="10-15", month_of_year="*")
        with self.assertRaises(ValidationError) as err:
            periodic.save()
        self.assertTrue("Cannot define both interval and crontab schedule." in err.exception.message)

    def test_collection_name(self):
        app = Celery()
        app.conf.update(**{"mongodb_scheduler_collection": "schedules2"})
        import celerybeatmongo
        importlib.reload(celerybeatmongo)
        importlib.reload(celerybeatmongo.models)
        from celerybeatmongo.models import PeriodicTask
        self.assertEqual("schedules2", PeriodicTask._get_collection().name)
