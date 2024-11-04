"""Stream type classes for tap-eventbrite."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_eventbrite.client import EventbriteStream

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class Organizations(EventbriteStream):
    """Organizations stream.

    https://www.eventbrite.com/platform/api#/reference/organization/list-your-organizations/list-your-organizations
    """

    name = "organizations"
    path = "/v3/users/me/organizations/"
    records_jsonpath = "$.organizations[*]"
    primary_keys = ("id",)
    replication_key = None

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="The organization id",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The organization name",
        ),
        th.Property(
            "vertical",
            th.StringType,
            description="The organization vertical",
        ),
        th.Property(
            "image_id",
            th.StringType,
            description="The organization image id",
        ),
    ).to_dict()

    def generate_child_contexts(
        self,
        record: dict[str, t.Any],
        context: Context | None,  # noqa: ARG002
    ) -> t.Iterable[Context | None]:
        """Generate child contexts."""
        yield {"organization_id": record["id"]}


class Events(EventbriteStream):
    """Events stream.

    https://www.eventbrite.com/platform/api#/reference/event/list/list-events-by-organization
    """

    name = "events"
    path = "/v3/organizations/{organization_id}/events/"
    records_jsonpath = "$.events[*]"
    primary_keys = ("id",)
    replication_key = None

    parent_stream_type = Organizations

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="Event id",
        ),
        th.Property(
            "name",
            th.ObjectType(
                th.Property("text", th.StringType),
                th.Property("html", th.StringType),
            ),
            description="Event name",
        ),
        th.Property(
            "summary",
            th.StringType,
            description=(
                "Event summary. This is a plaintext field and will have any supplied "
                "HTML removed from it. Maximum of 140 characters, mutually exclusive "
                "with description."
            ),
        ),
        th.Property(
            "description",
            th.ObjectType(
                th.Property("text", th.StringType),
                th.Property("html", th.StringType),
            ),
            description=(
                "(DEPRECATED) Event description (contents of the event page). May be "
                "long and have significant formatting. Clients may choose to skip "
                "retrieving the event description by enabling the API switch "
                "OMIT_DESCRIPTION_FROM_EVENT_CONTAINER, which will result in the "
                "description being returned as null."
            ),
        ),
        th.Property(
            "start",
            th.ObjectType(
                th.Property("timezone", th.StringType, description="The timezone"),
                th.Property(
                    "utc",
                    th.DateTimeType,
                    description="The time relative to UTC",
                ),
                th.Property(
                    "local",
                    th.DateTimeType,
                    description="The time in the timezone of the event",
                ),
            ),
            description="Start date/time of the event",
        ),
        th.Property(
            "end",
            th.ObjectType(
                th.Property("timezone", th.StringType, description="The timezone"),
                th.Property(
                    "utc",
                    th.DateTimeType,
                    description="The time relative to UTC",
                ),
                th.Property(
                    "local",
                    th.DateTimeType,
                    description="The time in the timezone of the event",
                ),
            ),
            description="End date/time of the event",
        ),
        th.Property(
            "url",
            th.URIType,
            description="The URL to the event page for this event on Eventbrite",
        ),
        th.Property(
            "vanity_url",
            th.StringType,
            description="The vanity URL to the event page for this event on Eventbrite",
        ),
        th.Property(
            "created",
            th.DateTimeType,
            description="When the event was created",
        ),
        th.Property(
            "changed",
            th.DateTimeType,
            description="When the event was last changed",
        ),
        th.Property(
            "published",
            th.DateTimeType,
            description="When the event was first published",
        ),
        th.Property(
            "status",
            th.StringType,
            description="Status of the event",
        ),
        th.Property(
            "currency",
            th.StringType,
            description="The ISO 4217 currency code for this event",
        ),
        th.Property(
            "online_event",
            th.BooleanType,
            description="If this event doesn't have a venue and is only held online",
        ),
        th.Property(
            "organization_id",
            th.StringType,
            description="Organization owning the event",
        ),
        th.Property(
            "organizer_id",
            th.StringType,
            description="Organization owning the event",
        ),
        th.Property(
            "logo_id",
            th.StringType,
            description="Image ID of the event logo",
        ),
        th.Property(
            "venue_id",
            th.StringType,
            description="Event venue ID",
        ),
        th.Property(
            "format_id",
            th.StringType,
            description="Event format",
        ),
        th.Property(
            "category_id",
            th.StringType,
            description="Event category",
        ),
        th.Property(
            "subcategory_id",
            th.StringType,
            description="Event subcategory",
        ),
        th.Property(
            "music_properties",
            th.ObjectType(
                th.Property(
                    "age_restriction",
                    th.StringType,
                    description="Minimum age requirement of event attendees.",
                ),
                th.Property(
                    "presented_by",
                    th.StringType,
                    description="Main music event sponsor.",
                ),
                th.Property(
                    "door_time",
                    th.DateTimeType,
                    description=(
                        "Time relative to UTC that the doors are opened to allow "
                        "people in the day of the event. When not set the event won't "
                        "have any door time set."
                    ),
                ),
            ),
            description=(
                "This is an object of properties that detail dimensions of music "
                "events."
            ),
        ),
        th.Property(
            "bookmark_info",
            th.ObjectType(
                th.Property(
                    "bookmarked",
                    th.BooleanType,
                    description="User saved the event or not.",
                ),
            ),
            description="If the event is locked",
        ),
        th.Property("refund_policy", th.StringType),
        th.Property(
            "listed",
            th.BooleanType,
            description="Is this event publicly searchable on Eventbrite?",
        ),
        th.Property(
            "shareable",
            th.BooleanType,
            description="Can this event show social sharing buttons?",
        ),
        th.Property(
            "invite_only",
            th.BooleanType,
            description="Can only people with invites see the event page?",
        ),
        th.Property(
            "show_remaining",
            th.BooleanType,
            description="Should the event page show the number of tickets left?",
        ),
        th.Property(
            "capacity",
            th.IntegerType,
            description="Maximum number of people who can attend.",
        ),
        th.Property(
            "capacity_is_custom",
            th.BooleanType,
            description=(
                "If True, the value of capacity is a custom-set value; if False, "
                "it's a calculated value of the total of all ticket capacities."
            ),
        ),
        th.Property(
            "tx_time_limit",
            th.StringType,
            description="Maximum duration (in seconds) of a transaction",
        ),
        th.Property(
            "hide_start_date",
            th.BooleanType,
            description="Show when event starts",
        ),
        th.Property(
            "hide_end_date",
            th.BooleanType,
            description="Hide when event ends",
        ),
        th.Property(
            "locale",
            th.StringType,
            description="The event Locale",
        ),
        th.Property(
            "is_locked",
            th.BooleanType,
            description="If the event is locked",
        ),
        th.Property(
            "privacy_setting",
            th.StringType,
            description="Privacy setting of the event",
        ),
        th.Property(
            "is_externally_ticketed",
            th.BooleanType,
            description="If the event is externally ticketed",
        ),
        th.Property(
            "external_ticketing",
            th.ObjectType(
                th.Property(
                    "external_url",
                    th.StringType,
                    description="The URL clients can follow to purchase tickets",
                ),
                th.Property(
                    "ticketing_provider_name",
                    th.StringType,
                    description="The name of the ticketing provider",
                ),
                th.Property(
                    "is_free",
                    th.BooleanType,
                    description=(
                        "Whether this is a free event. Mutually exclusive with ticket "
                        "price range."
                    ),
                ),
                th.Property(
                    "minimum_ticket_price",
                    th.ObjectType(
                        th.Property(
                            "currency",
                            th.StringType,
                            description="The ISO 4217 3-character code of a currency",
                        ),
                        th.Property(
                            "value",
                            th.NumberType,
                            description=(
                                "The integer value of units of the minor unit of the "
                                "currency (e.g. cents for US dollars)"
                            ),
                        ),
                        th.Property(
                            "major_value",
                            th.StringType,
                            description=(
                                "The integer value of units of the major unit of the "
                                "currency (e.g. dollars for US dollars)"
                            ),
                        ),
                        th.Property(
                            "display",
                            th.StringType,
                            description=(
                                "Provided for your convenience; its formatting may "
                                "change depending on the locale you query the API "
                                "with (for example, commas for decimal separators in "
                                "European locales)."
                            ),
                        ),
                    ),
                    description="The lowest price at which tickets are being sold.",
                ),
                th.Property(
                    "maximum_ticket_price",
                    th.ObjectType(
                        th.Property(
                            "currency",
                            th.StringType,
                            description="The ISO 4217 3-character code of a currency",
                        ),
                        th.Property(
                            "value",
                            th.NumberType,
                            description=(
                                "The integer value of units of the minor unit of the "
                                "currency (e.g. cents for US dollars)"
                            ),
                        ),
                        th.Property(
                            "major_value",
                            th.StringType,
                            description=(
                                "The integer value of units of the major unit of the "
                                "currency (e.g. dollars for US dollars)"
                            ),
                        ),
                        th.Property(
                            "display",
                            th.StringType,
                            description=(
                                "Provided for your convenience; its formatting may "
                                "change depending on the locale you query the API "
                                "with (for example, commas for decimal separators in "
                                "European locales)."
                            ),
                        ),
                    ),
                ),
                th.Property(
                    "sales_start",
                    th.DateTimeType,
                    description="When sales start",
                ),
                th.Property(
                    "sales_end",
                    th.DateTimeType,
                    description="When sales end",
                ),
            ),
        ),
        th.Property(
            "is_series",
            th.BooleanType,
            description="If the event is part of a series",
        ),
        th.Property(
            "is_series_parent",
            th.BooleanType,
            description="If the event is part of a series and is the series parent",
        ),
        th.Property(
            "series_id",
            th.StringType,
            description=(
                "If the event is part of a series, this is the event id of the series "
                "parent"
            ),
        ),
        th.Property(
            "is_reserved_seating",
            th.BooleanType,
            description="If the events has been set to have reserved seatings",
        ),
        th.Property(
            "show_pick_a_seat",
            th.BooleanType,
            description="Enables to show pick a seat option",
        ),
        th.Property(
            "show_seatmap_thumbnail",
            th.BooleanType,
            description="Enables to show seat map thumbnail",
        ),
        th.Property(
            "show_colors_in_seatmap_thumbnail",
            th.BooleanType,
            description="For reserved seating event, if venue map thumbnail should have colors on the event page.",  # noqa: E501
        ),
        th.Property(
            "is_free",
            th.BooleanType,
            description="Allows to set a free event",
        ),
        th.Property(
            "source",
            th.StringType,
            description="Source of the event (defaults to API)",
        ),
        th.Property("version", th.StringType),
        th.Property(
            "resource_uri",
            th.BooleanType,
            description=(
                "Is an absolute URL to the API endpoint that will return you the "
                "canonical representation of the event."
            ),
        ),
        th.Property(
            "event_sales_status",
            th.ObjectType(
                th.Property(
                    "sales_status",
                    th.StringType,
                    description="Sales status of the event",
                ),
                th.Property(
                    "start_sales_date",
                    th.ObjectType(
                        th.Property(
                            "timezone",
                            th.StringType,
                            description="The timezone",
                        ),
                        th.Property(
                            "utc",
                            th.DateTimeType,
                            description="The time relative to UTC",
                        ),
                        th.Property(
                            "local",
                            th.DateTimeType,
                            description="The time in the timezone of the event",
                        ),
                    ),
                    description="When sales start",
                ),
                th.Property(
                    "message",
                    th.StringType,
                    description=(
                        "Custom message associated with the current event sales status"
                    ),
                ),
                th.Property(
                    "message_type",
                    th.StringType,
                    description="Message type",
                ),
                th.Property(
                    "message_code",
                    th.StringType,
                    description="Message code",
                ),
            ),
            description=(
                "Additional data about the sales status of the event (optional)."
            ),
        ),
        th.Property(
            "checkout_settings",
            th.ObjectType(
                th.Property(
                    "created",
                    th.DateTimeType,
                    description="When the checkout settings object was created",
                ),
                th.Property(
                    "changed",
                    th.DateTimeType,
                    description="When the checkout settings object was last changed",
                ),
                th.Property(
                    "country_code",
                    th.StringType,
                    description="The ISO 3166 alpha-2 code of the country within which these checkout settings can apply.",  # noqa: E501
                ),
                th.Property(
                    "currency_code",
                    th.StringType,
                    description="The ISO 4217 3-character code of the currency for which these checkout settings can apply.",  # noqa: E501
                ),
                th.Property(
                    "checkout_method",
                    th.StringType,
                    description="The checkout method to use for completing consumer payment for tickets or other goods. Set of possible values [paypal, eventbrite, authnet, offline].",  # noqa: E501
                ),
                th.Property(
                    "offline_settings",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property(
                                "payment_method",
                                th.StringType(),
                                description="Set of possible values: [CASH, CHECK, INVOICE]",  # noqa: E501
                            ),
                            th.Property("instructions", th.StringType),
                        ),
                    ),
                    description="Offline checkout settings.",
                ),
                th.Property(
                    "user_instrument_vault_id",
                    th.StringType,
                    description="The merchant account user instrument ID for the checkout method. Only specify this value for PayPal and Authorize.net checkout settings.",  # noqa: E501
                ),
            ),
            description="Additional data about the checkout settings of the Event.",
        ),
    ).to_dict()

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        params = super().get_url_params(context, next_page_token)
        params["expand"] = "bookmark_info"
        return params
