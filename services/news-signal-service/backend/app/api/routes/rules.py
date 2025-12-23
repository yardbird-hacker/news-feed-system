from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    NotificationRuleCreate,
    NotificationRuleRead,
    NotificationChannelCreate,
)

from app.repositories.mysql.notification_rules_repository import (
    MySQLNotificationRulesRepository,
)
from app.repositories.mysql.notification_channels_repository import (
    MySQLNotificationChannelsRepository,
)

#router = APIRouter(prefix="/rules", tags=["rules"])
router = APIRouter(prefix="/users", tags=["users"])

# -----------------------------
# Create rule (+ channels)
# -----------------------------

@router.post("/{user_id}/rules", response_model=NotificationRuleRead)
def create_rule(
    *,
    session: SessionDep,
    user_id: int,
    rule_in: NotificationRuleCreate,
) -> Any:
    """
    Create a new notification rule with channels.
    """

    rules_repo = MySQLNotificationRulesRepository()
    channels_repo = MySQLNotificationChannelsRepository()

    # 1️⃣ 중복 rule 방지
    existing = rules_repo.get_by_user_and_keyword(
        user_id=user_id,
        keyword=rule_in.keyword,
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Rule with this keyword already exists",
        )

    # 2️⃣ Rule 생성
    rule = rules_repo.create(
        rule=rule_in.to_db(user_id=user_id)
    )

    # 3️⃣ Channel 생성
    for channel_in in rule_in.channels:
        channels_repo.create(
            channel=channel_in.to_db(rule_id=rule.id)
        )

    return NotificationRuleRead.from_db(rule)


# -----------------------------
# Get my rules
# -----------------------------
@router.get("/", response_model=List[NotificationRuleRead])
def read_my_rules(
    *,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Retrieve all notification rules for current user.
    """
    rules_repo = MySQLNotificationRulesRepository()
    rules = rules_repo.get_by_user(current_user.id)
    return [NotificationRuleRead.from_db(r) for r in rules]


# -----------------------------
# Delete rule (+ cascade channels)
# -----------------------------
@router.delete("/{rule_id}")
def delete_rule(
    *,
    rule_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Delete a rule and its channels.
    """
    rules_repo = MySQLNotificationRulesRepository()

    rule = rules_repo.get_by_id(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    if rule.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    rules_repo.delete(rule_id)
    return {"message": "Rule deleted successfully"}
