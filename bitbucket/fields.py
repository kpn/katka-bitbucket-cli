from datetime import datetime

from django.utils.timezone import make_aware

from rest_framework.fields import DateTimeField

from . import constants


def get_unix_timestamp(value: int) -> int:
    """
    Converts the given timestamp to seconds from a lower unit

    Args:
        value(int): the timestamp

    Returns:
        int: the unix timestamp

    """
    if value <= constants.MAX_TIMESTAMP:
        return value

    return get_unix_timestamp(value // 10)


class KatkaDateTimeField(DateTimeField):
    def to_representation(self, value):
        if isinstance(value, int):
            value = make_aware(datetime.fromtimestamp(get_unix_timestamp(value)))
        return super().to_representation(value)
