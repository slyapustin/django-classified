# -*- coding:utf-8 -*-

from datetime import datetime as dt, timedelta
from socket import error as socket_error

from django.core.management.base import BaseCommand

from proj.settings import DCF_ITEM_MAX_AGE_DAYS, EMAIL_HOST_USER
from dcf.models import Item


INT_DAYS_BEFORE_START_NOTIFICATION = 2  # before 2 day

NOTIFICATION_DAY = dt.today() - timedelta(
    days=(INT_DAYS_BEFORE_START_NOTIFICATION- (DCF_ITEM_MAX_AGE_DAYS or 0)))
NON_ACTIVE_DAY = dt.now() - timedelta(days=-DCF_ITEM_MAX_AGE_DAYS or 0)


class Command(BaseCommand):
    """
    Command for status change and notification users
    """
    help = 'Check status per day '

    def handle(self, *args, **options):
        """ Sending messages """
        if DCF_ITEM_MAX_AGE_DAYS is None:
            return
        items = Item.objects.select_related('user')
        for item in items.filter(
                posted__gte=NOTIFICATION_DAY.date(),
                posted__lt=NON_ACTIVE_DAY.date(),
        ).iterator():
            try:
                item.user.email_user(
                    # subject
                    '{slug}:{title} will deactivated '
                    'after 2 day'.format(**item.__dict__),
                    # message
                    'Your article "{slug}:{title} '
                    'is already outdated'
                    'Your article will be '
                    'deactivated after two days'.format(**item.__dict__),
                    # from_email
                    EMAIL_HOST_USER,
                )
            except socket_error:
                # TODO : Ask about the behavior in this case
                pass
        # Update message status
        items.filter(
            posted__gte=NON_ACTIVE_DAY.date()
        ).filter(is_active=True).update(is_active=False)

