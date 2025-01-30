
from django.core.management.base import BaseCommand

from openlxp_P1_notification.management.utils.p1ps_requests import (
    get_team_templates)


class Command(BaseCommand):
    """Django command to send an emails to the filer/personas, when the log
    warning/error occurred in the metadata EVTVL process."""

    def handle(self, *args, **options):
        """Load email templates from P1PS"""
        get_team_templates()
