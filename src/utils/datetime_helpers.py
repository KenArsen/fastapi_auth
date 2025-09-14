from datetime import datetime, timedelta, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def get_expiration_time(minutes: int = None) -> datetime:
    return utc_now() + timedelta(minutes=minutes)
