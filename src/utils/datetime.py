import datetime


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


def get_expiration_time(minutes: int = None) -> datetime.datetime:
    return utc_now() + datetime.timedelta(minutes=minutes)
