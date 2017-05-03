# -*- coding:utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.core.mail import send_mass_mail
from django.utils import timezone
from django.conf import settings
from django.db.models import Max
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext as _

from dcf.models import Item, CustomUser

class Command(BaseCommand):
    help = 'Remove old items'

    def emailsend(self, recipient):
        email_sender = settings.DEFAULT_FROM_EMAIL
        email_subject = _('Your items have been deactivated')

        msg_list = []

        for user in recipient:

            ctx = {'items': user.item_set.filter(user_id=user.id),
                'domain': '{}{}'.format(settings.DCF_SITE_SCHEMA,
                                        Site.objects.get_current().domain),
                }

            message = get_template('email_alert.html').render(Context(ctx))

            msg_list.append((email_subject,
                            message,
                            email_sender,
                            [user.email]))

        send_mass_mail(msg_list, fail_silently=False)


    def handle(self, *args, **options):

        remove_before = timezone.now() \
            - timezone.timedelta(days=settings.DCF_ITEM_MAX_AGE_DAYS)

        users = CustomUser.objects.filter\
            (item__updated__lte=remove_before, item__is_active=True)

        self.emailsend(users)

        Item.objects.filter\
            (updated__lte=remove_before).update(is_active=False)

