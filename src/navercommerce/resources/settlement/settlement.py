"""Settlement resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._types import NotGiven, not_given
from ...types.settlement import SettlementResponse

if TYPE_CHECKING:
    pass


class Settlement(SyncAPIResource):
    """
    Settlement resource for financial reporting.

    This resource provides access to:
    - Commission details by order
    - Daily settlement summaries
    - VAT reporting (daily and by case)
    - Settlement by case number
    """

    def get_commission_details(
        self,
        *,
        start_date: str,
        end_date: str,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> SettlementResponse:
        """
        Get commission breakdown details.

        Args:
            start_date: Settlement start date (YYYY-MM-DD format)
            end_date: Settlement end date (YYYY-MM-DD format)
            page: Page number for pagination
            size: Page size for pagination
            **kwargs: Additional query parameters

        Returns:
            SettlementResponse with commission details

        Example:
            ```python
            result = client.settlement.get_commission_details(
                start_date="2024-01-01",
                end_date="2024-01-31",
                page=0,
                size=100
            )
            for item in result.elements:
                print(f"Commission: {item}")
            ```
        """
        params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return self._get(
            "/v1/pay-settle/settle/commission-details",
            cast_to=SettlementResponse,
            options={"params": params},
        )

    def get_daily_settlement(
        self,
        *,
        start_date: str,
        end_date: str,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> SettlementResponse:
        """
        Get daily settlement summaries.

        Args:
            start_date: Settlement start date (YYYY-MM-DD format)
            end_date: Settlement end date (YYYY-MM-DD format)
            page: Page number for pagination
            size: Page size for pagination
            **kwargs: Additional query parameters

        Returns:
            SettlementResponse with daily settlement data

        Example:
            ```python
            result = client.settlement.get_daily_settlement(
                start_date="2024-01-01",
                end_date="2024-01-31"
            )
            for day in result.elements:
                print(f"Settlement for day: {day}")
            ```
        """
        params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return self._get(
            "/v1/pay-settle/settle/daily",
            cast_to=SettlementResponse,
            options={"params": params},
        )

    def get_vat_daily(
        self,
        *,
        start_date: str,
        end_date: str,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> SettlementResponse:
        """
        Get daily VAT reports.

        Args:
            start_date: Settlement start date (YYYY-MM-DD format)
            end_date: Settlement end date (YYYY-MM-DD format)
            page: Page number for pagination
            size: Page size for pagination
            **kwargs: Additional query parameters

        Returns:
            SettlementResponse with daily VAT data

        Example:
            ```python
            result = client.settlement.get_vat_daily(
                start_date="2024-01-01",
                end_date="2024-01-31"
            )
            for vat_record in result.elements:
                print(f"VAT: {vat_record}")
            ```
        """
        params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return self._get(
            "/v1/pay-settle/vat/daily",
            cast_to=SettlementResponse,
            options={"params": params},
        )

    def get_case_settlement(
        self,
        *,
        start_date: str,
        end_date: str,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> SettlementResponse:
        """
        Get settlement details by case number.

        Args:
            start_date: Settlement start date (YYYY-MM-DD format)
            end_date: Settlement end date (YYYY-MM-DD format)
            page: Page number for pagination
            size: Page size for pagination
            **kwargs: Additional query parameters

        Returns:
            SettlementResponse with case-based settlement data

        Example:
            ```python
            result = client.settlement.get_case_settlement(
                start_date="2024-01-01",
                end_date="2024-01-31"
            )
            for case in result.elements:
                print(f"Case settlement: {case}")
            ```
        """
        params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return self._get(
            "/v1/pay-settle/settle/case",
            cast_to=SettlementResponse,
            options={"params": params},
        )

    def get_vat_case(
        self,
        *,
        start_date: str,
        end_date: str,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> SettlementResponse:
        """
        Get VAT details by case number.

        Args:
            start_date: Settlement start date (YYYY-MM-DD format)
            end_date: Settlement end date (YYYY-MM-DD format)
            page: Page number for pagination
            size: Page size for pagination
            **kwargs: Additional query parameters

        Returns:
            SettlementResponse with case-based VAT data

        Example:
            ```python
            result = client.settlement.get_vat_case(
                start_date="2024-01-01",
                end_date="2024-01-31"
            )
            for vat_case in result.elements:
                print(f"VAT case: {vat_case}")
            ```
        """
        params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return self._get(
            "/v1/pay-settle/vat/case",
            cast_to=SettlementResponse,
            options={"params": params},
        )


class AsyncSettlement(AsyncAPIResource):
    """
    Async settlement resource for financial reporting.

    This resource provides async access to:
    - Commission details by order
    - Daily settlement summaries
    - VAT reporting (daily and by case)
    - Settlement by case number
    """

    async def get_commission_details(
        self,
        *,
        start_date: str,
        end_date: str,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> SettlementResponse:
        """Get commission breakdown details."""
        params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return await self._get(
            "/v1/pay-settle/settle/commission-details",
            cast_to=SettlementResponse,
            options={"params": params},
        )

    async def get_daily_settlement(
        self,
        *,
        start_date: str,
        end_date: str,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> SettlementResponse:
        """Get daily settlement summaries."""
        params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return await self._get(
            "/v1/pay-settle/settle/daily",
            cast_to=SettlementResponse,
            options={"params": params},
        )

    async def get_vat_daily(
        self,
        *,
        start_date: str,
        end_date: str,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> SettlementResponse:
        """Get daily VAT reports."""
        params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return await self._get(
            "/v1/pay-settle/vat/daily",
            cast_to=SettlementResponse,
            options={"params": params},
        )

    async def get_case_settlement(
        self,
        *,
        start_date: str,
        end_date: str,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> SettlementResponse:
        """Get settlement details by case number."""
        params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return await self._get(
            "/v1/pay-settle/settle/case",
            cast_to=SettlementResponse,
            options={"params": params},
        )

    async def get_vat_case(
        self,
        *,
        start_date: str,
        end_date: str,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> SettlementResponse:
        """Get VAT details by case number."""
        params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return await self._get(
            "/v1/pay-settle/vat/case",
            cast_to=SettlementResponse,
            options={"params": params},
        )
