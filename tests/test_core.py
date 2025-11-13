"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

from typing import Any

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_eventbrite.tap import TapEventbrite

SAMPLE_CONFIG: dict[str, Any] = {}

TestTapEventbrite = get_tap_test_class(
    TapEventbrite,
    config=SAMPLE_CONFIG,
    suite_config=SuiteConfig(
        max_records_limit=10,
        ignore_no_records_for_streams=[
            "events",
        ],
    ),
)
