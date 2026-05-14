from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class KrxClientConfig:
    base_url: str = "https://data.krx.co.kr"


class KrxClient:
    """KRX-style market data adapter template.

    The demo package does not perform network calls. Use this template to transform real
    market prices into `market_quarterly.csv` fields such as stock_return_3m,
    volatility_3m, and volume_change_3m.
    """

    def __init__(self, config: KrxClientConfig | None = None):
        self.config = config or KrxClientConfig()

    def normalize_market_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("Connect real KRX market-data normalization before production use")
