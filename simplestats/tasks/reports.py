'''
Email the site admins a report for the past day
'''

import datetime
import logging

from celery.schedules import crontab
from celery.task.base import periodic_task

from simplestats.models import Report

from django.contrib.auth.models import User
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

SPACER = '\n' + '-' * 80 + '\n'


@periodic_task(run_every=crontab(minute=0, hour=7))
def daily_report():
    today = datetime.datetime.utcnow().replace(microsecond=0, second=0)
    # FIXME: Better date handling without -1 day shim
    now = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    today = now.replace(microsecond=0, second=0, minute=0, hour=0).date()

    reports = [report.text for report in Report.objects.filter(date=today)]
    recipient_list = [user.email for user in User.objects.filter(is_superuser=True)]

    if not recipient_list:
        logger.info('Empty recipient list. Skipping Daily Report')
        return

    if not reports:
        logger.info('Empty report list. Skipping Daily Report')
        return

    send_mail(
        'Daily Report',
        message=SPACER.join(reports),
        from_email='django@tsundere.co',
        recipient_list=recipient_list,
    )
