from datetime import datetime
from sqlalchemy import select
from app.models import Item


def find_matched_news(
    session,
    *,
    keyword: str,
    since: datetime,
    limit: int = 5,
):
    stmt = (
        select(Item)
        # .where(Item.keyword.ilike(f"%{keyword}%"))
        .where(Item.created_at > since)
        .order_by(Item.created_at.desc())
        .limit(limit)
    )
    return session.execute(stmt).scalars().all()
