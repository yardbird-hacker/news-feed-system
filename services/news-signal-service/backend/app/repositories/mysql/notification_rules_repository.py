import logging
from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.models import NotificationRuleDB
from app.repositories.notification_rules_repository import (
    NotificationRulesRepository,
)

logger = logging.getLogger(__name__)


class MySQLNotificationRulesRepository(NotificationRulesRepository):
    """
    MySQL implementation of NotificationRulesRepository.
    """

    def __init__(self):
        self._session_factory = SessionLocal

    def create(self, rule: NotificationRuleDB) -> NotificationRuleDB:
        session: Session = self._session_factory()
        try:
            sql = text(
                """
                INSERT INTO notification_rules (user_id, keyword, is_active)
                VALUES (:user_id, :keyword, :is_active)
                """
            )
            session.execute(
                sql,
                {
                    "user_id": rule.user_id,
                    "keyword": rule.keyword,
                    "is_active": rule.is_active,
                },
            )
            session.commit()

            rule.id = session.execute(
                text("SELECT LAST_INSERT_ID()")
            ).scalar_one()

            logger.debug(
                "Created notification rule (id=%s, user_id=%s, keyword=%s)",
                rule.id,
                rule.user_id,
                rule.keyword,
            )
            return rule

        except Exception:
            session.rollback()
            logger.exception(
                "Failed to create notification rule (user_id=%s, keyword=%s)",
                rule.user_id,
                rule.keyword,
            )
            raise
        finally:
            session.close()

    def get_by_id(self, rule_id: int) -> Optional[NotificationRuleDB]:
        session: Session = self._session_factory()
        try:
            sql = text("SELECT * FROM notification_rules WHERE id = :id")
            row = session.execute(sql, {"id": rule_id}).mappings().first()
            return NotificationRuleDB(**row) if row else None
        finally:
            session.close()

    def get_by_user(self, user_id: int) -> List[NotificationRuleDB]:
        session: Session = self._session_factory()
        try:
            sql = text(
                "SELECT * FROM notification_rules WHERE user_id = :user_id"
            )
            rows = session.execute(sql, {"user_id": user_id}).mappings().all()
            return [NotificationRuleDB(**row) for row in rows]
        finally:
            session.close()

    def get_by_user_and_keyword(
        self, user_id: int, keyword: str
    ) -> Optional[NotificationRuleDB]:
        session: Session = self._session_factory()
        try:
            sql = text(
                """
                SELECT * FROM notification_rules
                WHERE user_id = :user_id AND keyword = :keyword
                """
            )
            row = session.execute(
                sql, {"user_id": user_id, "keyword": keyword}
            ).mappings().first()
            return NotificationRuleDB(**row) if row else None
        finally:
            session.close()

    def delete(self, rule_id: int) -> None:
        session: Session = self._session_factory()
        try:
            session.execute(
                text("DELETE FROM notification_rules WHERE id = :id"),
                {"id": rule_id},
            )
            session.commit()
            logger.debug("Deleted notification rule (id=%s)", rule_id)
        except Exception:
            session.rollback()
            logger.exception(
                "Failed to delete notification rule (id=%s)", rule_id
            )
            raise
        finally:
            session.close()
