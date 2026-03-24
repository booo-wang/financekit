"""Cryptocurrency crawler wrapper."""

from datetime import datetime
from typing import List

from .base import BaseCrawler
from .yahoo_finance import YahooFinanceCrawler
from ..models import CryptoData, StockData
from ..utils import setup_logger

logger = setup_logger(__name__)


class CryptoCrawler(BaseCrawler):
    """Fetch cryptocurrency data through Yahoo Finance."""

    SUPPORTED_SYMBOLS = {
        "BTC": "BTC-USD",
        "ETH": "ETH-USD",
        "BNB": "BNB-USD",
        "XRP": "XRP-USD",
        "ADA": "ADA-USD",
    }

    def __init__(self) -> None:
        """Initialise the crypto crawler."""
        super().__init__("Crypto Crawler")
        self.yahoo_crawler = YahooFinanceCrawler()

    def fetch_crypto_data(
        self, symbol: str, start_date: datetime, end_date: datetime
    ) -> List[CryptoData]:
        """Fetch cryptocurrency data for the requested symbol."""
        full_symbol = self.SUPPORTED_SYMBOLS.get(symbol.upper(), f"{symbol}-USD")

        logger.info(f"Fetching crypto data: {symbol} ({full_symbol})")
        return self.yahoo_crawler.fetch_crypto_data(full_symbol, start_date, end_date)

    def fetch_stock_data(
        self, symbol: str, start_date: datetime, end_date: datetime
    ) -> List[StockData]:
        """CryptoCrawler does not support stock symbols."""
        raise NotImplementedError(
            "CryptoCrawler does not support stock data, use YahooFinanceCrawler instead"
        )

    def get_supported_symbols(self) -> dict:
        """Return the supported crypto symbol mapping."""
        return self.SUPPORTED_SYMBOLS.copy()
