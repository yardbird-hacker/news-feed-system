from datetime import datetime, timedelta
from sqlalchemy import select

from app.core.db import SessionLocal
from app.models import (
    NotificationChannelDB,
    NotificationRuleDB,
    User,
)
from app.repositories.news import find_matched_news
from app.services.notification.email_sender import send_email
from app.services.notification.email_contents import build_email_content


def run():
    with SessionLocal() as session:
        stmt = (
            select(
                NotificationChannelDB,
                NotificationRuleDB,
                User,
            )
            .join(
                NotificationRuleDB,
                NotificationRuleDB.id == NotificationChannelDB.rule_id,
            )
            .join(
                User,
                User.id == NotificationRuleDB.user_id,
            )
            .where(NotificationChannelDB.is_active == True)
        )

        rows = session.execute(stmt).all()
        sent = 0

        for channel, rule, user in rows:
            # since = channel.last_sent_at or (
            #     datetime.utcnow() - timedelta(hours=240)
            # )
            since = datetime.utcnow() - timedelta(hours=240)

            news = find_matched_news(
                session,
                keyword=rule.keyword,
                since=since,
            )

            if not news:
                continue

            subject, body = build_email_content(
                user_name=user.name,
                keyword=rule.keyword,
                news_list=news,
            )

            send_email(
                to_email=user.email,
                subject=subject,
                body=body,
            )

            channel.last_sent_at = datetime.utcnow()
            session.add(channel)
            sent += 1

        session.commit()
        print(f"[DONE] sent={sent}")


if __name__ == "__main__":
    run()
