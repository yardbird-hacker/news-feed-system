from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class KeywordRepository(ABC):
    """
    Persistence abstraction for keyword index.
    """

    @abstractmethod
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
        """
        Persist a keyword index record.
        Must be idempotent.
        """
        raise NotImplementedError
