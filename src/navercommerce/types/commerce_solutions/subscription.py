"""Commerce Solutions subscription types."""

from __future__ import annotations

from pydantic import Field

from ..._models import BaseModel


class SubscriptionInfo(BaseModel):
    """Subscription information."""

    subscription_id: str | None = Field(None, alias="subscriptionId")
    account_uid: str | None = Field(None, alias="accountUid")
    status: str | None = None
    created_date: str | None = Field(None, alias="createdDate")

    model_config = {"extra": "allow"}


class SellerInfo(BaseModel):
    """Seller information from JWT token."""

    seller_id: str | None = Field(None, alias="sellerId")
    account_uid: str | None = Field(None, alias="accountUid")
    seller_name: str | None = Field(None, alias="sellerName")

    model_config = {"extra": "allow"}


class Transaction(BaseModel):
    """Commerce solutions transaction."""

    transaction_id: str | None = Field(None, alias="transactionId")
    transaction_type: str | None = Field(None, alias="transactionType")
    amount: int | None = None
    created_date: str | None = Field(None, alias="createdDate")

    model_config = {"extra": "allow"}


class SubscriptionResponse(BaseModel):
    """Subscription query response."""

    subscription: SubscriptionInfo | None = None

    model_config = {"extra": "allow"}


class TransactionResponse(BaseModel):
    """Transaction list response."""

    transactions: list[Transaction] = Field(default_factory=list)
    total_count: int | None = Field(None, alias="totalCount")

    model_config = {"extra": "allow"}
