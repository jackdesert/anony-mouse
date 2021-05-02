from datetime import datetime, timedelta
from uuid import uuid4

class TalkingStick:

    RESERVE_WINDOW_IN_SECONDS = 60

    # 0, 1, and 3 are states
    # 2 is a pseudostate

    AVAILABLE = 0
    RESERVED = 1
    # You can assume that RESERVED_BY_YOU is 2
    WAITING = 3


    _state = AVAILABLE
    _token = None
    _timestamp = None

    @classmethod
    def reset(cls):
        cls._state = cls.AVAILABLE
        cls._token = None
        cls._timestamp = None

    @classmethod
    def reserve(cls):
        """
        Reserve the talking stick if available
        """
        if cls._state == cls.AVAILABLE:
            cls._state = cls.RESERVED
            cls._token = str(uuid4())
            cls._timestamp = datetime.now()
            return dict(
                    # calling cls.state() so pseudostate is available
                    state=cls.state(cls._token),
                    token=cls._token,
                    seconds_remaining=cls.RESERVE_WINDOW_IN_SECONDS)
        return dict(state=cls._state)

    @classmethod
    def publish(cls, message, token):
        valid_or_not, reason = cls.is_token_valid(token)

        if valid_or_not:
            print(f'Publishing {message}')
            cls.reset()
        return valid_or_not, reason


    @classmethod
    def is_token_valid(cls, token):
        if cls._state != cls.RESERVED:
            return False, 'not currently reserved'
        if cls._token != token:
            return False, 'wrong token'
        now = datetime.now()
        time_remaining = timedelta(seconds=cls.RESERVE_WINDOW_IN_SECONDS) - (now - cls._timestamp)
        remaining_seconds = time_remaining.total_seconds()
        if remaining_seconds < 0:
            return False, 'token expired'
        return True, f'remaining_seconds: {remaining_seconds}'


    @classmethod
    def state(cls, token=''):
        """
        Returns the state or pseudostate
        """
        valid_or_not, unused_reason = cls.is_token_valid(token)
        return cls._state + bool(valid_or_not)





