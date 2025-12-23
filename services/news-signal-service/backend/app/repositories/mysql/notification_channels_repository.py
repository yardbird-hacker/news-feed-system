import logging
from datetime import datetime
from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.models import NotificationChannelDB
from app.repositories.notification_channels_repository import (
    NotificationChannelsRepository,
)


logger = logging.getLogger(__name__)


class MySQLNotificationChannelsRepository(NotificationChannelsRepository):
    """
    MySQL implementation of NotificationChannelsRepository.
    """

    def __init__(self):
        self._session_factory = SessionLocal

    def create(
        self, channel: NotificationChannelDB
    ) -> NotificationChannelDB:
        session: Session = self._session_factory()
        try:
            sql = text(
                """
                INSERT INTO notification_channels
                    (rule_id, channel, delivery_mode, frequency, last_sent_at, is_active)
                VALUES
                    (:rule_id, :channel, :delivery_mode, :frequency, :last_sent_at, :is_active)
                """
            )
            session.execute(
                sql,
                {
                    "rule_id": channel.rule_id,
                    "channel": channel.channel,
                    "delivery_mode": channel.delivery_mode,
                    "frequency": channel.frequency,
                    "last_sent_at": channel.last_sent_at,
                    "is_active": channel.is_active,
                },
            )
            session.commit()

            channel.id = session.execute(
                text("SELECT LAST_INSERT_ID()")
            ).scalar_one()

            logger.debug(
                "Created notification channel (id=%s, rule_id=%s, channel=%s)",
                channel.id,
                channel.rule_id,
                channel.channel,
            )
            return channel

        except Exception:
            session.rollback()
            logger.exception(
                "Failed to create notification channel (rule_id=%s, channel=%s)",
                channel.rule_id,
                channel.channel,
            )
            raise
        finally:
            session.close()

    def get_by_rule(self, rule_id: int) -> List[NotificationChannelDB]:
        session: Session = self._session_factory()
        try:
            sql = text(
                "SELECT * FROM notification_channels WHERE rule_id = :rule_id"
            )
            rows = session.execute(
                sql, {"rule_id": rule_id}
            ).mappings().all()
            return [NotificationChannelDB(**row) for row in rows]
        finally:
            session.close()

    def get_by_rule_and_channel(
        self, rule_id: int, channel: str
    ) -> Optional[NotificationChannelDB]:
        session: Session = self._session_factory()
        try:
            sql = text(
                """
                SELECT * FROM notification_channels
                WHERE rule_id = :rule_id AND channel = :channel
                """
            )
            row = session.execute(
                sql, {"rule_id": rule_id, "channel": channel}
            ).mappings().first()
            return NotificationChannelDB(**row) if row else None
        finally:
            session.close()

    def find_digest_due_channels(
        self, *, now: datetime
    ) -> List[NotificationChannelDB]:
        session: Session = self._session_factory()
        try:
            sql = text(
                """
                SELECT *
                FROM notification_channels
                WHERE delivery_mode = 'digest'
                  AND is_active = true
                  AND (
                        last_sent_at IS NULL
                        OR (
                            frequency = 'hourly'
                            AND last_sent_at <= :now - INTERVAL 1 HOUR
                        )
                        OR (
                            frequency = 'daily'
                            AND last_sent_at <= :now - INTERVAL 1 DAY
                        )
                  )
                """
            )
            rows = session.execute(sql, {"now": now}).mappings().all()
            return [NotificationChannelDB(**row) for row in rows]
        finally:
            session.close()

    def update_last_sent_at(
        self, channel_id: int, sent_at: datetime
    ) -> None:
        session: Session = self._session_factory()
        try:
            session.execute(
                text(
                    """
                    UPDATE notification_channels
                    SET last_sent_at = :sent_at
                    WHERE id = :id
                    """
                ),
                {"id": channel_id, "sent_at": sent_at},
            )
            session.commit()
            logger.debug(
                "Updated last_sent_at for channel (id=%s)", channel_id
            )
        except Exception:
            session.rollback()
            logger.exception(
                "Failed to update last_sent_at (id=%s)", channel_id
            )
            raise
        finally:
            session.close()

    def deactivate(self, channel_id: int) -> None:
        session: Session = self._session_factory()
        try:
            session.execute(
                text(
                    "UPDATE notification_channels SET is_active = false WHERE id = :id"
                ),
                {"id": channel_id},
            )
            session.commit()
            logger.debug("Deactivated notification channel (id=%s)", channel_id)
        except Exception:
            session.rollback()
            logger.exception(
                "Failed to deactivate notification channel (id=%s)", channel_id
            )
            raise
        finally:
            session.close()
