"""Yahoo Finance crawler."""

from datetime import datetime, timedelta
from typing import List

from .base import BaseCrawler
from ..models import StockData, CryptoData
from ..utils import setup_logger

logger = setup_logger(__name__)


class YahooFinanceCrawler(BaseCrawler):
    """Yahoo Finance data crawler."""

    BASE_URL = "https://query1.finance.yahoo.com"

    def __init__(self):
        super().__init__("Yahoo Finance Crawler")
        self.timeout = 10

    def fetch_stock_data(
        self, symbol: str, start_date: datetime, end_date: datetime
    ) -> List[StockData]:
        """Fetch stock data.

        Current implementation returns generated sample data.
        """
        try:
            logger.info(f"Fetching stock data: {symbol}")
            return self._generate_sample_stock_data(symbol, start_date, end_date)
        except Exception as exc:
            logger.error(f"Failed to fetch stock data: {exc}")
            return []

    def fetch_crypto_data(
        self, symbol: str, start_date: datetime, end_date: datetime
    ) -> List[CryptoData]:
        """Fetch crypto data.

        Current implementation returns generated sample data.
        """
        try:
            logger.info(f"Fetching crypto data: {symbol}")
            return self._generate_sample_crypto_data(symbol, start_date, end_date)
        except Exception as exc:
            logger.error(f"Failed to fetch crypto data: {exc}")
            return []

    @staticmethod
    def _generate_sample_stock_data(
        symbol: str, start_date: datetime, end_date: datetime
    ) -> List[StockData]:
        """Generate sample stock time-series data."""
        import random

        data = []
        current_date = start_date
        base_price = 100.0

        while current_date <= end_date:
            if current_date.weekday() >= 5:
                current_date += timedelta(days=1)
                continue

            change = random.uniform(-2, 2)
            open_price = base_price
            close_price = base_price * (1 + change / 100)
            high_price = max(open_price, close_price) * random.uniform(1.00, 1.02)
            low_price = min(open_price, close_price) * random.uniform(0.98, 1.00)

            stock_data = StockData(
                symbol=symbol,
                date=current_date,
                open=round(open_price, 2),
                high=round(high_price, 2),
                low=round(low_price, 2),
                close=round(close_price, 2),
                volume=int(random.uniform(1_000_000, 10_000_000)),
            )

            data.append(stock_data)
            base_price = close_price
            current_date += timedelta(days=1)

        return data

    @staticmethod
    def _generate_sample_crypto_data(
        symbol: str, start_date: datetime, end_date: datetime
    ) -> List[CryptoData]:
        """Generate sample crypto time-series data."""
        import random

        data = []
        current_date = start_date
        base_price = 50000.0 if symbol == "BTC-USD" else 3000.0

        while current_date <= end_date:
            change = random.uniform(-3, 3)
            open_price = base_price
            close_price = base_price * (1 + change / 100)
            high_price = max(open_price, close_price) * random.uniform(1.00, 1.03)
            low_price = min(open_price, close_price) * random.uniform(0.97, 1.00)

            crypto_data = CryptoData(
                symbol=symbol,
                date=current_date,
                open=round(open_price, 2),
                high=round(high_price, 2),
                low=round(low_price, 2),
                close=round(close_price, 2),
                volume=random.uniform(10_000_000, 100_000_000),
                market_cap=round(close_price * random.uniform(1e10, 1e12), 2),
            )

            data.append(crypto_data)
            base_price = close_price
            current_date += timedelta(days=1)

        return data
