from typing import Dict
from django.http import HttpRequest
import datetime
import pytz


def session_check(request: HttpRequest, sessionId: str) -> str:
    if request.session.exists(sessionId):
        session_expiry_date = request.session.get_expiry_date()
        current_date = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
        if current_date < session_expiry_date:
            return "login"
        else:
            request.session.clear_expired()
            return "expired"
    else:
        return "notExist"

