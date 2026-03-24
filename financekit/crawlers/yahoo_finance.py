"""Yahoo Finance crawler using yfinance for real market data."""

from datetime import datetime
from pathlib import Path
from typing import List

import yfinance as yf

from .base import BaseCrawler
from ..models import StockData, CryptoData
from ..utils import setup_logger

logger = setup_logger(__name__)
YFINANCE_CACHE_DIR = Path(__file__).resolve().parents[2] / "cache" / "yfinance"


def _configure_yfinance_cache() -> None:
    """Keep yfinance's sqlite cache in a writable project-local directory."""
    YFINANCE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    yf.set_tz_cache_location(str(YFINANCE_CACHE_DIR))


class YahooFinanceCrawler(BaseCrawler):
    """Yahoo Finance data crawler fetching real market data via yfinance."""

    def __init__(self):
        super().__init__("Yahoo Finance Crawler")
        self.timeout = 10

    def fetch_stock_data(
        self, symbol: str, start_date: datetime, end_date: datetime
    ) -> List[StockData]:
        """Fetch real stock data from Yahoo Finance.

        Args:
            symbol: Stock ticker symbol (e.g. 'AAPL', 'MSFT')
            start_date: Start date for historical data
            end_date: End date for historical data

        Returns:
            List of StockData with real market prices
        """
        try:
            _configure_yfinance_cache()
            logger.info(f"Fetching stock data: {symbol}")
            ticker = yf.Ticker(symbol)
            df = ticker.history(
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
            )

            if df.empty:
                logger.warning(f"No data returned for {symbol}")
                return []

            data = []
            for date, row in df.iterrows():
                stock_data = StockData(
                    symbol=symbol,
                    date=date.to_pydatetime().replace(tzinfo=None),
                    open=round(float(row["Open"]), 2),
                    high=round(float(row["High"]), 2),
                    low=round(float(row["Low"]), 2),
                    close=round(float(row["Close"]), 2),
                    volume=int(row["Volume"]),
                )
                data.append(stock_data)

            logger.info(f"Fetched {len(data)} records for {symbol}")
            return data

        except Exception as exc:
            logger.error(f"Failed to fetch stock data for {symbol}: {exc}")
            return []

    def fetch_crypto_data(
        self, symbol: str, start_date: datetime, end_date: datetime
    ) -> List[CryptoData]:
        """Fetch real cryptocurrency data from Yahoo Finance.

        Args:
            symbol: Crypto symbol (e.g. 'BTC-USD', 'ETH-USD')
            start_date: Start date for historical data
            end_date: End date for historical data

        Returns:
            List of CryptoData with real market prices
        """
        try:
            _configure_yfinance_cache()
            logger.info(f"Fetching crypto data: {symbol}")
            ticker = yf.Ticker(symbol)
            df = ticker.history(
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
            )

            if df.empty:
                logger.warning(f"No data returned for {symbol}")
                return []

            # Try to get market cap from ticker info
            market_cap = None
            try:
                info = ticker.info
                market_cap = info.get("marketCap")
            except Exception:
                pass

            data = []
            for date, row in df.iterrows():
                crypto_data = CryptoData(
                    symbol=symbol,
                    date=date.to_pydatetime().replace(tzinfo=None),
                    open=round(float(row["Open"]), 2),
                    high=round(float(row["High"]), 2),
                    low=round(float(row["Low"]), 2),
                    close=round(float(row["Close"]), 2),
                    volume=float(row["Volume"]),
                    market_cap=float(market_cap) if market_cap else None,
                )
                data.append(crypto_data)

            logger.info(f"Fetched {len(data)} records for {symbol}")
            return data

        except Exception as exc:
            logger.error(f"Failed to fetch crypto data for {symbol}: {exc}")
            return []
