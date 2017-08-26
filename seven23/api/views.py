"""
    Root views of api
"""

import json
from django.http import HttpResponse

from rest_framework.decorators import api_view

from seven23 import settings

@api_view(["GET"])
def api_init(request):
    """
        Return status on client initialisation
    """
    result = {}

    # Return API Version.
    result['api_version'] = settings.API_VERSION
    result['allow_account_creation'] = settings.ALLOW_ACCOUNT_CREATION
    result['contact'] = settings.CONTACT_EMAIL

    if request.user.is_authenticated():
        result['is_authenticated'] = True
        result['id'] = request.user.id
    else:
        result['is_authenticated'] = False

    # Return json format string.
    j = json.dumps(result, separators=(',', ':'))
    return HttpResponse(j, content_type='application/json')