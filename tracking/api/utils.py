from rest_framework.views import exception_handler as default_exception_handler
from rest_framework.response import Response
from rest_framework import status

from tracking.models import Session

from datetime import datetime, timedelta

import sys
import traceback
import uuid
import json
import requests as global_requests

import logging
logger = logging.getLogger('tracking')

def session_expires():
    return datetime.now() - timedelta(hours=1)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_or_create_session(request):
    ip_address = get_client_ip(request)
    platform = request.user_agent.os.family

    session = Session.objects.filter(
        ip_address__exact=ip_address
        ).last()

    cookie = session.cookie if session and session.cookie else '%s' % uuid.uuid4()

    geo_data = json.loads(global_requests.get('http://www.freegeoip.net/json/%s' % ip_address).content)

    session = Session.objects.update_or_create(
        ip_address__exact=ip_address,
        last_seen__gt=session_expires(),
        platform__exact=platform,
        defaults={
            'ip_address': ip_address,
            'platform': platform,
            'cookie': cookie,
            'country_name': geo_data['country_name'],
            'country_code': geo_data['country_code'],
            'city': geo_data['city'],
            'time_zone': geo_data['time_zone'],
            'latitude': geo_data['latitude'],
            'longitude': geo_data['longitude']
            }
        )

    return session[0]

def custom_exception_handler(exc, context):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    callstack = '\n'.join(traceback.format_tb(exc_traceback))
    errorlist = []
    errorlist.append('\n\nRequest URL: %s' % str(context['request']._request))
    errorlist.append('Error type: %s' % exc_type)
    errorlist.append('Error value: %s' % exc_value)
    errorlist.append('Payload: %s' % str(context['request'].query_params))
    errorlist.append('Message: %s' % exc.message)
    errorlist.append('----Call stack----\n %s' % callstack)
    errorlist.append('------Locals------\n %s' % str(context['request']._request.__dict__))
    errormsg = '\n'.join(errorlist)

    logger.error(errormsg)

    original_response = default_exception_handler(exc, context)

    if original_response is not None:
        return original_response
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=exc.message, content_type='application/json')