from setuptools import setup


setup(
    name="celerybeat-mongo",
    description="A Celery Beat Scheduler that uses MongoDB to store both schedule definitions and status information",
    version="0.2.0",
    license="Apache License, Version 2.0",
    author="Zakir Durumeric",
    author_email="zakird@gmail.com",
    maintainer="Zakir Durumeric",
    maintainer_email="zakird@gmail.com",
    keywords="python celery beat periodic task mongodb",
    packages=[
        "celerybeatmongo"
    ],
    install_requires=[
        'setuptools',
        'pymongo',
        'mongoengine',
        'celery',
        'blinker'
    ],
    classifiers=[
        'Development Status :: 2 - Production/Stable',
        'License :: Apache License 2.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Communications',
        'Topic :: System :: Distributed Computing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
    ]
)
