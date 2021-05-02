from threading import RLock

from pyramid.view import view_config
from amouse.models.talking_stick import TalkingStick

LOCK = RLock()


"""
Any interactions with TalkingStick are expected to be wrapped in LOCK
"""


@view_config(route_name='home', renderer='amouse:templates/index.jinja2')
def home_view(request):
    with LOCK:
        res = dict(state=TalkingStick.state())
        print(res)
        return res


@view_config(route_name='reserve', renderer='json')
def reserve_view(request):
    with LOCK:
        reservation = TalkingStick.reserve()
        print(reservation)
        return reservation


@view_config(route_name='publish', renderer='json')
def publish_view(request):
    message = request.json.get('message')
    token = request.json.get('token')
    with LOCK:
        success, reason = TalkingStick.publish(message, token)
        res = dict(success=success, reason=reason)
        print(res)
        return res


@view_config(route_name='state', renderer='json')
def state_view(request):
    token = request.json.get('token')
    with LOCK:
        res = dict(state=TalkingStick.state(token))
        return res
