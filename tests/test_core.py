"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_cmf_chile.tap import TapCMFChileAPIV3

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    # TODO: Initialize minimal tap config
}


# Run standard built-in tap tests from the SDK:
TestTapCMFChileAPIV3 = get_tap_test_class(
    tap_class=TapCMFChileAPIV3,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
