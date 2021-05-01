from datetime import datetime, timedelta
from uuid import uuid4
import os

import requests


class TalkingStick:

    RESERVE_WINDOW_IN_SECONDS = 10
    REGENERATE_TIME_IN_SECONDS = 20

    THEMES = ('What would it be like to ',
              'It would be great if ',
              'I would love to see ',
              'It\'s hard to watch ',
              'This is scary to say because ',
              'Testing:  1, 2, 3, 4!',)

    SLACK_HOOK = os.getenv('AMOUSE_SLACK_HOOK')
    if not SLACK_HOOK:
        raise RuntimeError('Must define a SLACK_HOOK')

    # 0, 1, and 3 are states
    # 2 is a pseudostate

    AVAILABLE = 0
    RESERVED = 1
    # You can assume that RESERVED_BY_YOU is 2
    REGENERATING = 3

    _state = AVAILABLE
    _token = None
    _timestamp = None

    @classmethod
    def _reset(cls):
        cls._state = cls.AVAILABLE
        cls._token = None
        cls._timestamp = None

    @classmethod
    def themes_dict(cls):
        """
        :return: :dict:
        """
        output = {}
        for index, item in enumerate(cls.THEMES):
            output[str(index)] = item
        return output


    @classmethod
    def reserve(cls):
        """
        Reserve the talking stick if available
        """
        if cls._state == cls.AVAILABLE:
            cls._state = cls.RESERVED
            cls._token = str(uuid4())
            cls._timestamp = datetime.now()
            return cls.state_dict(cls._token)
        return cls.state_dict()

    @classmethod
    def publish(cls, message, token, theme_index):
        valid_or_not, reason = cls.is_token_valid(token)

        if valid_or_not:
            cls._send_to_slack(message, theme_index)
            print(f'Publishing {message}')
            cls._reset()
        return cls.state_dict()

    @classmethod
    def _send_to_slack(cls, message, theme_index):
        try:
            theme = cls.THEMES[theme_index]
        except IndexError:
            theme = cls.THEMES[0]
        text = f'*{theme}*\n{message}'
        payload=dict(text=text)
        requests.post(cls.SLACK_HOOK, json=payload)

    def _payload(self, long_ago):
        snippet = 'Long Ago' if long_ago else ''
        text = f'{self.site} is {self.status} {snippet}'
        print(f'Notified: "{text}"')

        return dict(text=text,
                    icon_emoji='ghost')



    @classmethod
    def _token_seconds_remaining(cls):
        """
        Returns the number of seconds the token is still valid.
        A negative number indicates token is invalid.

        :return: :float:
        """
        return cls._seconds_remaining(cls.RESERVE_WINDOW_IN_SECONDS)

    @classmethod
    def _regenerate_seconds_remaining(cls):
        """
        Returns the number of seconds until the talking stick regenerates
        A negative number time to change state

        :return: :float:
        """
        # TODO change state if negative number
        return cls._seconds_remaining(cls.REGENERATE_TIME_IN_SECONDS)

    @classmethod
    def _seconds_remaining(cls, original_seconds):
        """
        Returns a positive or negative number
        """
        if cls._timestamp is None:
            return -1000
        now = datetime.now()
        time_remaining = timedelta(seconds=original_seconds) - (now - cls._timestamp)
        seconds = time_remaining.total_seconds()
        return seconds

    @classmethod
    def is_token_valid(cls, token):
        if cls._state != cls.RESERVED:
            return False, 'not currently reserved'
        if cls._token != token:
            return False, 'wrong token'
        seconds = cls._token_seconds_remaining()
        if seconds < 0:
            return False, 'token expired'
        return True, seconds

    @classmethod
    def state_tuple(cls, token=''):
        """
        Returns a tuple containing:
            A. The state
            B. Seconds remaining (or None)
            C. Token (or None)


        """
        # First check for stale reservations
        if (cls._state == cls.RESERVED) and (cls._token_seconds_remaining() < 0):
            cls._reset()

        valid_or_not, token_seconds_remaining = cls.is_token_valid(token)
        if (cls._state == cls.RESERVED) and valid_or_not:
            # Return a pseudostate
            return cls._state + 1, token_seconds_remaining, token
        regen_seconds = cls._regenerate_seconds_remaining()
        if (cls._state == cls.REGENERATING) and (regen_seconds < 0):
            # Change state to AVAILABLE because waited long enough
            cls._state = cls.AVAILABLE
        if cls._state == cls.REGENERATING:
            return cls._state, regen_seconds, None
        return cls._state, None, None

    @classmethod
    def state_dict(cls, token=''):
        """
        Returns state and seconds remaining
        """
        state, seconds_remaining, returned_token = cls.state_tuple(token)
        return dict(
            state=state, seconds_remaining=seconds_remaining, token=returned_token
        )
