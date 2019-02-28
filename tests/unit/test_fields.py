import pytest
from bitbucket.fields import KatkaDateTimeField, get_unix_timestamp


@pytest.mark.parametrize(
    'timestamp, expected_timestamp',
    (
        (1549274354000, 1549274354),
        (0, 0),
        (1549274354, 1549274354),
        (9999999999, 9999999999),
        (99999999991, 9999999999),
    )
)
def test_get_unix_timestamp(timestamp, expected_timestamp):
    assert get_unix_timestamp(timestamp) == expected_timestamp


class TestKatkaDateTimeField:
    @pytest.mark.parametrize(
        'timezone, expected_datetime',
        (
            ('UTC', '2019-02-04T10:23:12Z'),
            ('CET', '2019-02-04T11:23:12+01:00'),
        )
    )
    def test_int_to_representation(self, timezone, expected_datetime, settings):
        settings.TIME_ZONE = timezone

        assert KatkaDateTimeField().to_representation(1549275792000) == expected_datetime

    @pytest.mark.parametrize(
        'datetime, expected_datetime',
        (
            ('2019-02-04T10:23:12Z', '2019-02-04T10:23:12Z'),
            ('2019-02-04T10:23:12+01:00', '2019-02-04T10:23:12+01:00'),
        )
    )
    def test_str_to_representation(self, datetime, expected_datetime, settings):
        settings.TIME_ZONE = 'UTC'

        assert KatkaDateTimeField().to_representation(datetime) == expected_datetime
