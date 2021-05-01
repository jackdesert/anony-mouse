from threading import RLock
import json

from pyramid.view import view_config
from amouse.models.talking_stick import TalkingStick

LOCK = RLock()


"""
Any interactions with TalkingStick are expected to be wrapped in LOCK
"""


@view_config(route_name='home', renderer='amouse:templates/index.jinja2')
def home_view(request):
    context = dict(themes_json=json.dumps(TalkingStick.themes_dict()))
    return context


@view_config(route_name='reserve', renderer='json')
def reserve_view(request):
    with LOCK:
        reservation = TalkingStick.reserve()
        print(reservation)
        return reservation


@view_config(route_name='publish', renderer='json')
def publish_view(request):
    blob = request.json

    message = blob.get('message')
    token = blob.get('token')
    theme_index = int(blob.get('theme_index'))

    with LOCK:
        state_dict = TalkingStick.publish(message, token, theme_index)
        print(state_dict)
        return state_dict


@view_config(route_name='state', renderer='json')
def state_view(request):
    token = request.json.get('token')
    with LOCK:
        state_dict = TalkingStick.state_dict(token)
        return state_dict
