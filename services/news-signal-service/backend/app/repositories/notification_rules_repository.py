from abc import ABC, abstractmethod
from typing import List, Optional

from app.models import NotificationRuleDB


class NotificationRulesRepository(ABC):
    """
    Persistence abstraction for notification rules.
    (user × keyword)
    """

    @abstractmethod
    def create(self, rule: NotificationRuleDB) -> NotificationRuleDB:
        """Create a new notification rule."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, rule_id: int) -> Optional[NotificationRuleDB]:
        """Get a rule by id."""
        raise NotImplementedError

    @abstractmethod
    def get_by_user(self, user_id: int) -> List[NotificationRuleDB]:
        """Get all rules for a user."""
        raise NotImplementedError

    @abstractmethod
    def get_by_user_and_keyword(
        self, user_id: int, keyword: str
    ) -> Optional[NotificationRuleDB]:
        """Get a rule by user and keyword."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, rule_id: int) -> None:
        """Delete a rule."""
        raise NotImplementedError
