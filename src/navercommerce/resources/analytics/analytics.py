"""Analytics resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Dict, List

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._types import NotGiven, not_given

if TYPE_CHECKING:
    from ..._client import AsyncNaverCommerce, NaverCommerce


class MarketingAnalytics(SyncAPIResource):
    """Marketing analytics sub-resource for brand store performance data."""

    def get_all_daily(
        self,
        *,
        channel_no: str,
        start_date: str,
        end_date: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Get all channel daily marketing stats."""
        params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }
        params.update(kwargs)
        
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/all/daily",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_all_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get all channel detailed marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/all/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_custom_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get custom channel detailed stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/custom/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_custom_simple(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get custom channel simple stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/custom/simple",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_hourly_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get hourly detailed marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/hourly/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_hourly_simple(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get hourly simple marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/hourly/simple",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_search_keyword(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get search keyword marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/search/keyword",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_search_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get search detailed marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/search/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_website_daily(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get website daily marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/website/daily",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_website_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get website detailed marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/website/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )


class SalesAnalytics(SyncAPIResource):
    """Sales analytics sub-resource for sales performance data."""

    def get_realtime_daily(
        self, *, channel_no: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get realtime daily sales stats."""
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/realtime/daily",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )

    def get_delivery_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get delivery detailed sales stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/sales/delivery/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_product_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get product detailed sales stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/sales/product/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_hourly_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get hourly detailed sales stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/sales/hourly/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_shopping_page_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get shopping page detailed stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/shopping/page/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    def get_shopping_product_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get shopping product detailed stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/shopping/product/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )


class Analytics(SyncAPIResource):
    """
    Analytics resource for business intelligence and reporting.

    This resource provides access to:
    - Marketing analytics (traffic, channels, campaigns)
    - Sales analytics (revenue, products, delivery)
    """

    @cached_property
    def marketing(self) -> MarketingAnalytics:
        """Access marketing analytics sub-resource."""
        return MarketingAnalytics(self._client)

    @cached_property
    def sales(self) -> SalesAnalytics:
        """Access sales analytics sub-resource."""
        return SalesAnalytics(self._client)


# Async versions
class AsyncMarketingAnalytics(AsyncAPIResource):
    """Async marketing analytics sub-resource."""

    async def get_all_daily(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get all channel daily marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/all/daily",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_all_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get all channel detailed marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/all/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_custom_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get custom channel detailed stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/custom/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_custom_simple(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get custom channel simple stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/custom/simple",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_hourly_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get hourly detailed marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/hourly/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_hourly_simple(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get hourly simple marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/hourly/simple",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_search_keyword(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get search keyword marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/search/keyword",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_search_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get search detailed marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/search/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_website_daily(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get website daily marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/website/daily",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_website_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get website detailed marketing stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/marketing/website/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )


class AsyncSalesAnalytics(AsyncAPIResource):
    """Async sales analytics sub-resource."""

    async def get_realtime_daily(
        self, *, channel_no: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get realtime daily sales stats."""
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/realtime/daily",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )

    async def get_delivery_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get delivery detailed sales stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/sales/delivery/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_product_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get product detailed sales stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/sales/product/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_hourly_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get hourly detailed sales stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/sales/hourly/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_shopping_page_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get shopping page detailed stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/shopping/page/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )

    async def get_shopping_product_detail(
        self, *, channel_no: str, start_date: str, end_date: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get shopping product detailed stats."""
        params: Dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        params.update(kwargs)
        return await self._get(
            f"/v1/bizdata-stats/channels/{channel_no}/shopping/product/detail",
            cast_to=dict,  # type: ignore
            options={"params": params},
        )


class AsyncAnalytics(AsyncAPIResource):
    """Async analytics resource for business intelligence."""

    @cached_property
    def marketing(self) -> AsyncMarketingAnalytics:
        """Access async marketing analytics sub-resource."""
        return AsyncMarketingAnalytics(self._client)

    @cached_property
    def sales(self) -> AsyncSalesAnalytics:
        """Access async sales analytics sub-resource."""
        return AsyncSalesAnalytics(self._client)
