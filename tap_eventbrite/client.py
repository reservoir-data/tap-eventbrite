"""REST client handling, including EventbriteStream base class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from singer_sdk import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import JSONPathPaginator

if TYPE_CHECKING:
    from requests import Response
    from singer_sdk.helpers.types import Context


class EventbritePaginator(JSONPathPaginator):
    """Eventbrite paginator class."""

    @override
    def has_more(self, response: Response) -> bool:
        """Return True if there are more pages available."""
        pagination = response.json().get("pagination", {})
        return pagination.get("has_more_items", False)  # type: ignore[no-any-return]


class EventbriteStream(RESTStream[Any]):
    """Eventbrite stream class."""

    @override
    @property
    def url_base(self) -> str:
        """The API URL root, configurable via tap settings."""
        return self.config["base_url"]  # type: ignore[no-any-return]

    @override
    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        return BearerTokenAuthenticator(token=self.config["token"])

    @override
    def get_new_paginator(self) -> EventbritePaginator:
        return EventbritePaginator(jsonpath="$.pagination.continuation")

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, Any]:
        return {
            "continuation": next_page_token,
        }
