from datetime import datetime
from sqlmodel import select, Session

from app.models import NotificationChannelDB


def get_active_channels(session: Session):
    stmt = select(NotificationChannelDB).where(
        NotificationChannelDB.is_active == True
    )
    
    result = session.execute(stmt)
    return result.scalars().all()


def mark_channel_sent(
    session: Session,
    channel: NotificationChannelDB,
    sent_at: datetime,
):
    channel.last_sent_at = sent_at
    session.add(channel)
