
Django Background Tasks (Async Update)

Django Background Task is a database-backed work queue for Django, loosely based around `Ruby's DelayedJob`_ library. This project was adopted and adapted from lilspikey_ `django-background-task` and updated to fix thread concurrency. 

.. _Ruby's DelayedJob: https://github.com/tobi/delayed_job
.. _lilspikey: https://github.com/lilspikey/

You can find in PyPI as django-background-tasks-async-update.

In Django Background Task, all tasks are implemented as functions (or any other callable).

There are two parts to using background tasks:

- creating the task functions and registering them with the scheduler
- setup a cron task (or long running process) to execute the tasks


Docs
====
See `Read the docs`_.

.. _Read the docs: http://django-background-tasks.readthedocs.io/en/latest/

