"""CMFChileAPIV3 tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_cmf_chile import streams


class TapCMFChileAPIV3(Tap):
    """CMFChileAPIV3 tap class."""

    name = "tap-cmf-chile"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "apikey",
            th.StringType,
            required=True,
            secret=True,
            description="The token to authenticate against CMF API v3",
        ),
        th.Property(
            "start_date",
            th.DateType,
            required=True,
            description="The earliest record date to sync",
        )
    ).to_dict()

    def discover_streams(self) -> list[streams.CMFChileAPIV3Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.UFStream(self),
            streams.UTMStream(self),
            streams.DolarStream(self),
        ]


if __name__ == "__main__":
    TapCMFChileAPIV3.cli()
