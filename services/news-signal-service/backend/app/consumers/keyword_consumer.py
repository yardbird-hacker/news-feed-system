import json
import logging
from kafka import KafkaConsumer

from app.core.config import settings
from app.services.keyword_service import KeywordService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run():
    logger.info("Starting keyword consumer...")
    #logger.info("Received keyword event: %s", event)
    consumer = KafkaConsumer(
        settings.KAFKA_KEYWORD_TOPIC,               # "keyword.indexed"
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="news.keyword.g1",
        enable_auto_commit=False,                   # 중요
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )


    service = KeywordService()

    for message in consumer:
        event = message.value
        logger.info("Received keyword event: %s", event)

        try:
            # 핵심: consumer는 처리 위임만 한다
            service.handle(event)

            # 처리 성공 시에만 offset commit
            consumer.commit()

        except Exception as e:
            logger.exception("Failed to process keyword event: %s", event)
            # commit 안 함 → 재처리됨 (at-least-once)
            continue


if __name__ == "__main__":
    run()
