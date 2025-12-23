from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from app.models import NotificationChannelDB


class NotificationChannelsRepository(ABC):
    """
    Persistence abstraction for notification delivery channels.
    (rule × channel)
    """

    @abstractmethod
    def create(self, channel: NotificationChannelDB) -> NotificationChannelDB:
        """Create a delivery channel for a rule."""
        raise NotImplementedError

    @abstractmethod
    def get_by_rule(self, rule_id: int) -> List[NotificationChannelDB]:
        """Get all channels for a rule."""
        raise NotImplementedError

    @abstractmethod
    def get_by_rule_and_channel(
        self, rule_id: int, channel: str
    ) -> Optional[NotificationChannelDB]:
        """Get a specific channel for a rule."""
        raise NotImplementedError

    @abstractmethod
    def find_digest_due_channels(
        self, *, now: datetime
    ) -> List[NotificationChannelDB]:
        """
        Find channels that should send digest notifications now.
        Used by cron job.
        """
        raise NotImplementedError

    @abstractmethod
    def update_last_sent_at(
        self, channel_id: int, sent_at: datetime
    ) -> None:
        """Update last_sent_at after successful delivery."""
        raise NotImplementedError

    @abstractmethod
    def deactivate(self, channel_id: int) -> None:
        """Disable a channel."""
        raise NotImplementedError
