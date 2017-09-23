# -*- coding:utf-8 -*-
"""
Scheduled command: updates statuses and sends messages
"""

from datetime import datetime as dt, timedelta

import sys
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.translation import ugettext as _

from dcf.models import Item, CustomUser


DCF_ITEM_MAX_AGE_DAYS = settings.DCF_ITEM_MAX_AGE_DAYS or 0

timedelta_start_notification_period = timedelta(
    days=settings.INT_DAYS_BEFORE_START_NOTIFICATION-(
        DCF_ITEM_MAX_AGE_DAYS))

timedelta_end_notification_period = timedelta_start_notification_period + (
    timedelta(days=settings.DAY))

notification_period = [
    dt.now() + timedelta_start_notification_period,
    dt.now() + timedelta_end_notification_period]


timedelta_deadline_transfer_to_archive = timedelta(
    days=-DCF_ITEM_MAX_AGE_DAYS)

non_active_day = dt.now() + timedelta_deadline_transfer_to_archive

admin_mail = settings.ADMINS[0][1]


def summary_body_send_message(
        list_of_dicts, subject, msg_template, from_email, to_email, **kwargs):
    """
    Function populate message body and then mail it

    :param list_of_dicts: [{"world": "hello"}, ]
    :param subject: letter subject
    :param msg_template: text with one pointed formatting brackets " The {}"
    :param from_email:
    :param to_email:
    :return:
    """
    msg_body_with_articles = ''
    for dict_ in list_of_dicts:
        msg_body_with_articles += _(', '.join(dict_.values()) + '<br>')
    send_mail(
        # subject
        _(subject),
        # message
        _(msg_template.format(msg_body_with_articles)),
        # from_email
        from_email,
        # to user email
        [to_email],
        **kwargs
    )


class Command(BaseCommand):
    """
    Command for status change and notification users
    """
    help = 'Check status per day '

    def handle(self, *args, **options):
        """ Sending messages """
        if settings.DCF_ITEM_MAX_AGE_DAYS is None:
            return
        custom_users_with_out_of_date_items = CustomUser.objects.filter(
            id__in=Item.objects.filter(
                Q(posted__range=notification_period) |
                Q(posted__lte=non_active_day.date()),
                is_active=True
            ).values('user_id'))

        for custom_user in custom_users_with_out_of_date_items:

            list_of_dicts_where_posted_in_notification_period = (
                custom_user.item_set.filter(
                    posted__range=notification_period
                ).values('title', 'slug')
            )
            if list_of_dicts_where_posted_in_notification_period.exists():
                summary_body_send_message(
                    # list_of_dicts
                    list_of_dicts_where_posted_in_notification_period,
                    # subject
                    'Out of date articles. '
                    'Your articles will be deactivated soon. ',
                    # msg_template,
                    'Your articles: {} '
                    'is already outdated.'
                    'Your article will be '
                    'deactivated after two days',
                    # from_email
                    admin_mail,
                    # to user email
                    custom_user.email,
                    fail_silently=True
                )

            list_of_dicts_where_posted_older_non_active_day = (
                custom_user.item_set.filter(
                    posted__lte=non_active_day.date()
                ).values('title', 'slug')
            )
            if list_of_dicts_where_posted_older_non_active_day.exists():
                summary_body_send_message(
                    # list_of_dicts
                    list_of_dicts_where_posted_older_non_active_day,
                    # subject
                    'Out of date articles. '
                    'Your articles is already deactivated',
                    # msg_template,
                    'Your articles: {} has been '
                    'moved to the archive.',
                    # from_email
                    admin_mail,
                    # to user email
                    custom_user.email,
                    fail_silently=True
                )
                list_of_dicts_where_posted_older_non_active_day.update(
                    is_active=False)
