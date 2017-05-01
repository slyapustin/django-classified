# -*- coding:utf-8 -*-

from datetime import datetime as dt, timedelta
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail


from dcf.models import Item

DAY = 1
INT_DAYS_BEFORE_START_NOTIFICATION = 2 * DAY

timedelta_start_notification_period = timedelta(
    days=INT_DAYS_BEFORE_START_NOTIFICATION-(
        settings.DCF_ITEM_MAX_AGE_DAYS or 0))

timedelta_end_notification_period = timedelta_start_notification_period + (
    timedelta(days=DAY))

notification_period = [
    dt.now() + timedelta_start_notification_period,
    dt.now() + timedelta_end_notification_period]

NON_ACTIVE_DAY = dt.now() - timedelta(
    days=-settings.DCF_ITEM_MAX_AGE_DAYS or 0)


class Command(BaseCommand):
    """
    Command for status change and notification users
    """
    help = 'Check status per day '

    def handle(self, *args, **options):
        """ Sending messages """
        if settings.DCF_ITEM_MAX_AGE_DAYS is None:
            return
        items = Item.objects.select_related('user')
        for item in items.filter(
                posted__range=notification_period,
                is_active=True):
            # Send message : will be deactivated soon
            send_mail(
                # subject
                _(
                    '{slug}:{title} will be '
                    'deactivated soon'.format(**item.__dict__)
                ),
                # message
                _(
                    'Your article "{slug}:{title} '
                    'is already outdated'
                    'Your article will be '
                    'deactivated after two days'.format(**item.__dict__)
                ),
                # from_email
                settings.EMAIL_HOST_USER,
                # to user email
                item.user.email,
                fail_silently=True
            )
        # Send message and Update message status
        queryset_turn_off_items = items.filter(
            posted__gte=NON_ACTIVE_DAY.date(),
            is_active=True
        )
        for turn_off_item in queryset_turn_off_items:
            send_mail(
                # subject
                _(
                    '{slug}:{title} is already '
                    'deactivated'.format(**item.__dict__)
                ),
                # message
                _(
                    'Your article {slug}:{title} has been '
                    'moved to the archive'.format(**item.__dict__)
                ),
                # from_email
                settings.EMAIL_HOST_USER,
                # to user email
                turn_off_item.user.email,
                fail_silently=True
            )
            queryset_turn_off_items.update(is_active=False)

