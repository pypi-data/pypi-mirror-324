import logging
import os

import requests

from requests.auth import AuthBase

from openlxp_P1_notification_project import settings

logger = logging.getLogger('dict_config_logger')

headers = {'Content-Type': 'application/json'}


"""
    Functions set up to extract environment values for
    Platform One Postal Service (P1PS) API

"""


def get_P1PS_base_endpoint():
    """Extracts P1PS base endpoint"""

    P1PS_domain = settings.P1PS_BASE_URL

    if P1PS_domain:
        # P1PS_endpoint = "https://" + P1PS_domain
        logger.info("P1PS endpoint value  is present and set")
    else:
        logger.error(P1PS_domain)
        logger.error("P1PS endpoint value is absent and not set")

    return P1PS_domain


def get_P1PS_team_token():
    """Extracts P1PS base endpoint"""
    team_token = settings.P1PS_AUTH_TOKEN

    if team_token:
        logger.info("Team Token value  is present and set")
    else:
        logger.error(team_token)
        logger.error("Team Token value is absent and not set")

    return team_token


def get_P1PS_team_ID():
    """Extracts P1PS base endpoint"""
    team_id = settings.P1PS_TEAM_ID

    if team_id:
        logger.info("Team ID value  is present and set")
    else:
        logger.error(team_id)
        logger.error("Team ID value is absent and not set")

    return team_id


"""
    Configuration set up for Platform One Postal Service (P1PS)
    API requests

"""


class TokenAuth(AuthBase):
    """Attaches HTTP Authentication Header to the given Request object."""

    def __call__(self, r, token_name='EMAIL_AUTH'):
        # modify and return the request

        r.headers[token_name] = get_P1PS_team_token()
        return r


def SetCookies():
    """Sets requests cookies jar with P1 authorization cookies"""
    logger.info("Setting cookies for email request P1ps")

    jar = requests.cookies.RequestsCookieJar()
    if os.environ.get('COOKIE_NAME') and os.environ.get('COOKIE_VALUE'):
        jar.set(os.environ.get('COOKIE_NAME'),
                os.environ.get('COOKIE_VALUE'),
                domain=settings.P1PS_BASE_URL, path='/')
    logger.info(jar)

    return jar
