import logging
from datetime import datetime, timezone

from app.repositories.keyword_repository import KeywordRepository
from app.repositories.mysql.keyword_repository import MySQLKeywordRepository

logger = logging.getLogger(__name__)


class KeywordService:
    """
    Keyword index processing service.
    - validation
    - light processing / normalization
    - persistence via repository
    """

    def __init__(self, repository: KeywordRepository | None = None):
        # 기본은 MySQL, 나중에 DynamoDB로 교체 가능
        self.repository = repository or MySQLKeywordRepository()

    def handle(self, event: dict) -> None:
        """
        Entry point called by Kafka consumer.
        Event example:
        {
          "news_id": 123,
          "keyword": "AI",
          "url": "https://news.site/...",
          "score": 0.92,
          "extractor_version": "v1.0",
          "created_at": 1734660000
        }
        """

        logger.debug("Handling keyword event: %s", event)

        data = self._validate_and_normalize(event)

        # persistence는 repository에게 위임
        self.repository.save(
            news_id=data["news_id"],
            keyword=data["keyword"],
            url=data["url"],
            score=data.get("score"),
            extractor_version=data.get("extractor_version"),
            created_at=data["created_at"],
        )

    # ------------------------
    # internal helpers
    # ------------------------

    def _validate_and_normalize(self, event: dict) -> dict:
        """
        Validate required fields and normalize data.
        여기서 processing 단계가 점점 늘어난다.
        """

        required_fields = ["news_id", "keyword", "url"]
        for field in required_fields:
            if field not in event:
                raise ValueError(f"Missing required field: {field}")

        # keyword normalization (아주 중요)
        keyword = event["keyword"].strip()
        if not keyword:
            raise ValueError("Empty keyword")

        # epoch seconds → datetime
        if "created_at" in event:
            created_at = datetime.fromtimestamp(
                event["created_at"], tz=timezone.utc
            )
        else:
            created_at = datetime.now(tz=timezone.utc)

        normalized = {
            "news_id": int(event["news_id"]),
            "keyword": keyword,
            "url": event["url"],
            "score": event.get("score"),
            "extractor_version": event.get("extractor_version"),
            "created_at": created_at,
        }

        logger.debug("Normalized keyword data: %s", normalized)
        return normalized
