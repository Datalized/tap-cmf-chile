"""Stream type classes for tap-cmf-chile."""

from __future__ import annotations

import typing as t
from pathlib import Path

import requests

from tap_cmf_chile.client import CMFChileAPIV3Stream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class UFStream(CMFChileAPIV3Stream):
    """Define custom stream."""

    name = "UF"
    path = "/uf/posteriores/{year}/{month}/dias/{day}"
    primary_keys: t.ClassVar[list[str]] = ["Fecha"]
    replication_key = "Fecha"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "uf.json"  # noqa: ERA001
    records_jsonpath = "$.UFs[*]"

    def get_url(self, context: dict | None) -> str:
        starting_date = self.get_starting_timestamp(context)
        url = "".join([self.url_base, self.path or ""])
        vals = {
            "year": starting_date.year,
            "month": starting_date.strftime('%m'),
            "day": starting_date.strftime('%m'),
        }
        for k, v in vals.items():
            search_text = "".join(["{", k, "}"])
            if search_text in url:
                url = url.replace(search_text, self._url_encode(v))
        self.logger.info("URL: %s", url)
        return url

    def validate_response(self, response: requests.Response) -> None:
        if response.status_code!=404:
            super().validate_response(response)

    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # convert to numeric
        row['Valor'] = row['Valor'].replace('.','').replace(',','.')
        row['Valor'] = float(row['Valor'])
        return row
