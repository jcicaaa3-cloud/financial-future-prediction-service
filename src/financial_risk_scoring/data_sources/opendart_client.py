from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OpenDartClientConfig:
    api_key: str
    base_url: str = "https://opendart.fss.or.kr/api"


class OpenDartClient:
    """Small adapter template for real-data ingestion.

    This class intentionally avoids network calls in the demo package. In a production
    version, connect `fetch_financial_statement` to OpenDART's financial statement APIs,
    normalize the response, and write the required CSV contract fields.
    """

    def __init__(self, config: OpenDartClientConfig):
        if not config.api_key:
            raise ValueError("OpenDART API key is required")
        self.config = config

    def build_financial_statement_url(self, *, corp_code: str, business_year: int, report_code: str) -> str:
        return (
            f"{self.config.base_url}/fnlttSinglAcntAll.json"
            f"?crtfc_key=***&corp_code={corp_code}&bsns_year={business_year}&reprt_code={report_code}&fs_div=CFS"
        )

    def normalize_financial_statement(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Normalize an OpenDART-like payload into the project CSV contract.

        Implement account-name mapping here when using real data.
        """
        raise NotImplementedError("Connect real OpenDART account mapping before production use")
