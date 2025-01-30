from datetime import datetime as dt
import json
import logging
import copy


from django.core.management.base import (BaseCommand, CommandParser,
                                         CommandError)

from openlxp_P1_notification.management.utils.p1ps_requests import (
    overall_health, send_email)
from openlxp_P1_notification.models import (email)

from openlxp_P1_notification.serializer import EmailSerializer

logger = logging.getLogger('dict_config_logger')


def trigger_health_check():
    """Command to trigger email health check"""
    overall_health()


def trigger_update(email_type, recipient_list, owner,
                                   list_name, list_url):
    """Command to trigger email for list updates"""

    trigger_health_check()

    now = dt.now()
    datetimenow = now.strftime("%d/%m/%Y %H:%M:%S")

    template_data = EmailSerializer(email_type).data

    for recipient_id in recipient_list:
        body_data = copy.deepcopy(template_data)

        body_data['recipients'] = [recipient_id[0]]
        name = recipient_id[1]
        author = owner

        if email_type.template_type.template_inputs:

            if 'name' in email_type.template_type.template_inputs:
                max_len = body_data['template_inputs']['name']['max_length']
                body_data['template_inputs']['name'] = name[:max_len]
            if 'datetime' in email_type.template_type.template_inputs:
                max_len = body_data['template_inputs']['datetime']['max_length']
                body_data['template_inputs']['datetime'] = datetimenow[:max_len]
            if 'list_name' in email_type.template_type.template_inputs:
                max_len = body_data['template_inputs']['list_name']['max_length']
                body_data['template_inputs']['list_name'] = list_name[:max_len]
            if 'list_url' in email_type.template_type.template_inputs:
                max_len = body_data['template_inputs']['list_url']['max_length']
                body_data['template_inputs']['list_url'] = list_url[:max_len]
            if 'author' in email_type.template_type.template_inputs:
                max_len = body_data['template_inputs']['author']['max_length']
                body_data['template_inputs']['author'] = author[:max_len]
        
        else:
            template_input = {"name" : name,
                              "datetime" : datetimenow,
                              "list_name" : list_name,
                              "list_url" : list_url,
                              "author" : author
                            }
            body_data['template_inputs'] = template_input

        body_data = json.dumps(body_data)

        send_email(body_data, str(email_type.template_type))


class Command(BaseCommand):
    """Django command to send an emails to the filer/personas, when the log
    warning/error occurred in the metadata EVTVL process."""

    def add_arguments(self, parser: CommandParser) -> None:
        # parser.add_argument('email_references', nargs="+", type=str)
        parser.add_argument('--email', type=str)
        parser.add_argument('--recipient-list', metavar='N',
                            type=str, nargs='+', help='a list of strings')

        return super().add_arguments(parser)

    def handle(self, *args, **options):
        """Email log notification is sent to filer/personas when warning/error
        occurred in EVTVL process"""
        # for email_reference in options['email_references']:
        try:
            email_type = email.objects.get(
                reference=options['email'])
        except email.DoesNotExist:
            raise CommandError('Email Reference "%s" does not exist' %
                               options['email'])

        trigger_update(email_type,
                       [tuple(options['recipient_list'])],
                       "Owner",
                       "List_Name",
                       "List_url")
