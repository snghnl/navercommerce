"""Commerce Solutions subscription types."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from ..._models import BaseModel


class SubscriptionInfo(BaseModel):
    """Subscription information."""

    subscription_id: Optional[str] = Field(None, alias="subscriptionId")
    account_uid: Optional[str] = Field(None, alias="accountUid")
    status: Optional[str] = None
    created_date: Optional[str] = Field(None, alias="createdDate")

    model_config = {"extra": "allow"}


class SellerInfo(BaseModel):
    """Seller information from JWT token."""

    seller_id: Optional[str] = Field(None, alias="sellerId")
    account_uid: Optional[str] = Field(None, alias="accountUid")
    seller_name: Optional[str] = Field(None, alias="sellerName")

    model_config = {"extra": "allow"}


class Transaction(BaseModel):
    """Commerce solutions transaction."""

    transaction_id: Optional[str] = Field(None, alias="transactionId")
    transaction_type: Optional[str] = Field(None, alias="transactionType")
    amount: Optional[int] = None
    created_date: Optional[str] = Field(None, alias="createdDate")

    model_config = {"extra": "allow"}


class SubscriptionResponse(BaseModel):
    """Subscription query response."""

    subscription: Optional[SubscriptionInfo] = None

    model_config = {"extra": "allow"}


class TransactionResponse(BaseModel):
    """Transaction list response."""

    transactions: List[Transaction] = Field(default_factory=list)
    total_count: Optional[int] = Field(None, alias="totalCount")

    model_config = {"extra": "allow"}
