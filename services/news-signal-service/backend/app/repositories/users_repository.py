from abc import ABC, abstractmethod
from typing import Optional

from app.models.user import UserDB


class UsersRepository(ABC):
    """
    Persistence abstraction for users.
    """

    @abstractmethod
    def create(self, user: UserDB) -> UserDB:
        """Create a new user."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserDB]:
        """Fetch a user by id."""
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserDB]:
        """Fetch a user by email."""
        raise NotImplementedError

    @abstractmethod
    def deactivate(self, user_id: int) -> None:
        """Deactivate a user."""
        raise NotImplementedError
