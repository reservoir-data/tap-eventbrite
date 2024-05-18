"""Eventbrite tap class."""

from __future__ import annotations

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_eventbrite import streams


class TapEventbrite(Tap):
    """Singer tap for Eventbrite."""

    name = "tap-eventbrite"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "token",
            th.StringType,
            required=True,
            description="API Token for Eventbrite",
        ),
        th.Property(
            "base_url",
            th.StringType,
            default="https://api.eventbrite.com",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
    ).to_dict()

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Eventbrite streams.
        """
        return [
            streams.Organizations(tap=self),
            streams.Events(tap=self),
        ]
