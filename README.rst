celerybeat-mongo
################

This is a `Celery Beat Scheduler <http://celery.readthedocs.org/en/latest/userguide/periodic-tasks.html/>`_
that stores both the schedules themselves and their status
information in a backend Mongo database. It can be installed by
installing the celerybeat-mongo Python egg::

    # pip install celerybeat-mongo

And specifying the scheduler when running Celery Beat, e.g.::

    $ celery beat -S celerybeatmongo.schedulers.MongoScheduler

Settings
########

The settings for the scheduler are defined in your celery configuration file
similar to how other aspects of Celery are configured:

* mongodb_scheduler_url: The mongodb `url <https://docs.mongodb.com/manual/reference/connection-string/>`_ connection used to store task results.
* mongodb_scheduler_db: The Mongodb database name
* mongodb_scheduler_collection (optional): the collection name used by model. If no value are specified, the default value will be used: **schedules**.

Usage
===================
Celerybeat-mongo just supports Interval and Crontab schedules.
Schedules easily can be manipulated using the mongoengine models in celerybeat mongo.models module.

Example creating interval-based periodic task
---------------------------------------------

To create a periodic task executing at an interval you must first
create the interval object::

    from celery import Celery

    config = {
        "mongodb_scheduler_db": "my_project",
        "mongodb_scheduler_url": "mongodb://localhost:27017",
    }

    app = Celery('hello', broker='redis://localhost//')
    app.conf.update(**config)

    from celerybeatmongo.models import PeriodicTask

    periodic = PeriodicTask(
        name='Importing contacts',
        task="proj.import_contacts"
        interval=PeriodicTask.Interval(every=10, period="seconds") # executes every 10 seconds.
    )
    periodic.save()

.. note::

    You should import celerybeat-mongo just after celery initialization.


Example creating crontab periodic task
---------------------------------------------

A crontab schedule has the fields: minute, hour, day_of_week, day_of_month and month_of_year, so if you want the equivalent of a 30 7 * * 1 (Executes every Monday morning at 7:30 a.m) crontab entry you specify::


    from celery import Celery

    config = {
        "mongodb_scheduler_db": "my_project",
        "mongodb_scheduler_url": "mongodb://localhost:27017",
    }

    app = Celery('hello', broker='redis://localhost//')
    app.conf.update(**config)

    from celerybeatmongo.models import PeriodicTask

    periodic = PeriodicTask(name="Send Email Notification", task="proj.notify_customers")
    periodic.crontab = PeriodicTask.Crontab(minute="30", hour="7", day_of_week="1",
                               day_of_month="0", month_of_year="*")
    periodic.save()
