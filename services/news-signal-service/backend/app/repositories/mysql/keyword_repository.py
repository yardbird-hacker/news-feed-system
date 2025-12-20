import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.repositories.keyword_repository import KeywordRepository

logger = logging.getLogger(__name__)


class MySQLKeywordRepository(KeywordRepository):
    """
    MySQL implementation of KeywordRepository.
    Uses INSERT ... ON DUPLICATE KEY UPDATE for idempotency.
    """

    def __init__(self):
        self._session_factory = SessionLocal

    def save(
        self,
        *,
        news_id: int,
        keyword: str,
        url: str,
        score: Optional[float],
        extractor_version: Optional[str],
        created_at: datetime,
    ) -> None:
        session: Session = self._session_factory()

        try:
            sql = text(
                """
                INSERT INTO news_keywords
                    (news_id, keyword, url, score, extractor_version, created_at)
                VALUES
                    (:news_id, :keyword, :url, :score, :extractor_version, :created_at)
                ON DUPLICATE KEY UPDATE
                    score = VALUES(score),
                    extractor_version = VALUES(extractor_version),
                    created_at = VALUES(created_at)
                """
            )

            session.execute(
                sql,
                {
                    "news_id": news_id,
                    "keyword": keyword,
                    "url": url,
                    "score": score,
                    "extractor_version": extractor_version,
                    "created_at": created_at,
                },
            )

            session.commit()
            logger.debug(
                "Saved keyword index (news_id=%s, keyword=%s)",
                news_id,
                keyword,
            )

        except Exception:
            session.rollback()
            logger.exception(
                "Failed to save keyword index (news_id=%s, keyword=%s)",
                news_id,
                keyword,
            )
            raise

        finally:
            session.close()
