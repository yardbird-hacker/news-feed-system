import logging
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.models.user import UserDB
from app.repositories.users_repository import UsersRepository

logger = logging.getLogger(__name__)


class MySQLUsersRepository(UsersRepository):
    """
    MySQL implementation of UsersRepository.
    """

    def __init__(self):
        self._session_factory = SessionLocal

    def create(self, user: UserDB) -> UserDB:
        session: Session = self._session_factory()
        try:
            sql = text(
                """
                INSERT INTO users (email, name, slack_user_id, is_active)
                VALUES (:email, :name, :slack_user_id, :is_active)
                """
            )

            session.execute(
                sql,
                {
                    "email": user.email,
                    "name": user.name,
                    "slack_user_id": user.slack_user_id,
                    "is_active": user.is_active,
                },
            )
            session.commit()

            user.id = session.execute(
                text("SELECT LAST_INSERT_ID()")
            ).scalar_one()

            logger.debug("Created user (id=%s, email=%s)", user.id, user.email)
            return user

        except Exception:
            session.rollback()
            logger.exception("Failed to create user (email=%s)", user.email)
            raise

        finally:
            session.close()

    def get_by_id(self, user_id: int) -> Optional[UserDB]:
        session: Session = self._session_factory()
        try:
            sql = text("SELECT * FROM users WHERE id = :id")
            row = session.execute(sql, {"id": user_id}).mappings().first()
            return UserDB(**row) if row else None
        finally:
            session.close()

    def get_by_email(self, email: str) -> Optional[UserDB]:
        session: Session = self._session_factory()
        try:
            sql = text("SELECT * FROM users WHERE email = :email")
            row = session.execute(sql, {"email": email}).mappings().first()
            return UserDB(**row) if row else None
        finally:
            session.close()

    def deactivate(self, user_id: int) -> None:
        session: Session = self._session_factory()
        try:
            sql = text(
                "UPDATE users SET is_active = false WHERE id = :id"
            )
            session.execute(sql, {"id": user_id})
            session.commit()
            logger.debug("Deactivated user (id=%s)", user_id)
        except Exception:
            session.rollback()
            logger.exception("Failed to deactivate user (id=%s)", user_id)
            raise
        finally:
            session.close()
