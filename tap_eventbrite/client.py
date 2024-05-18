"""REST client handling, including EventbriteStream base class."""

from __future__ import annotations

import typing as t

from singer_sdk import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import JSONPathPaginator

if t.TYPE_CHECKING:
    from requests import Response


class EventbritePaginator(JSONPathPaginator):
    """Eventbrite paginator class."""

    def has_more(self, response: Response) -> bool:
        """Return True if there are more pages available."""
        pagination = response.json().get("pagination", {})
        return pagination.get("has_more_items", False)  # type: ignore[no-any-return]


class EventbriteStream(RESTStream[t.Any]):
    """Eventbrite stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["base_url"]  # type: ignore[no-any-return]

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        token: str = self.config["token"]
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=token,
        )

    def get_new_paginator(self) -> EventbritePaginator:
        """Return a new paginator object.

        Returns:
            A paginator object.
        """
        return EventbritePaginator(jsonpath="$.pagination.continuation")

    @property
    def http_headers(self) -> dict[str, str]:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {"User-Agent": f"{self.tap_name}/{self._tap.plugin_version}"}

    def get_url_params(
        self,
        context: dict[str, t.Any] | None,  # noqa: ARG002
        next_page_token: str | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        params: dict[str, t.Any] = {
            "continuation": next_page_token,
        }
        return params
