from datetime import datetime, timedelta
from app.models import NotificationChannelDB


def should_send(channel: NotificationChannelDB, now: datetime) -> bool:
    # realtime → 항상
    if channel.delivery_mode == "realtime":
        return True

    # 첫 발송
    if channel.last_sent_at is None:
        return True

    delta = now - channel.last_sent_at

    if channel.frequency == "hourly":
        return delta >= timedelta(hours=1)

    if channel.frequency == "daily":
        return delta >= timedelta(days=1)

    return False
