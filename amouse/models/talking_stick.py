from datetime import datetime, timedelta
from uuid import uuid4


class TalkingStick:

    RESERVE_WINDOW_IN_SECONDS = 60
    REGENERATE_TIME_IN_SECONDS = 20

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
            return cls.state_dict(cls._token)
        return cls.state_dict()

    @classmethod
    def publish(cls, message, token):
        valid_or_not, reason = cls.is_token_valid(token)

        if valid_or_not:
            print(f'Publishing {message}')
            cls.reset()
        return cls.state_dict()

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
