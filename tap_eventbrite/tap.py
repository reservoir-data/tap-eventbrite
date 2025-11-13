"""Eventbrite tap class."""

from __future__ import annotations

from typing import override

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
            default="https://www.eventbriteapi.com",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[Stream]:
        return [
            streams.Organizations(tap=self),
            streams.Events(tap=self),
        ]
