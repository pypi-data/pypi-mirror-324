import logging
from django.urls import reverse
from openlxp_P1_notification.management.utils.p1ps_requests import (
    get_team_templates)

logger = logging.getLogger('dict_config_logger')


class TemplateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        admin_path = reverse('admin:index')

        if admin_path:
            admin_path = admin_path +'openlxp_P1_notification/template/'
        logger.info(admin_path)


        if request.path == "/admin/openlxp_P1_notification/template/" or \
            request.path == admin_path:
            try:
                get_team_templates()
            except TypeError as e:
                logger.error(e)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
