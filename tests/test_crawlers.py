"""Unit tests for crawler implementations."""

from datetime import datetime, timedelta
from unittest.mock import patch

import pandas as pd
import pytest

from financekit import CryptoCrawler, YahooFinanceCrawler


class FakeTicker:
    """Small yfinance stand-in used to keep tests offline and deterministic."""

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.info = {"marketCap": 123456789}

    def history(self, start: str, end: str) -> pd.DataFrame:
        dates = pd.date_range(start=start, periods=3, freq="D")
        return pd.DataFrame(
            {
                "Open": [100.0, 101.0, 102.0],
                "High": [101.0, 102.0, 103.0],
                "Low": [99.0, 100.0, 101.0],
                "Close": [100.5, 101.5, 102.5],
                "Volume": [1000, 1100, 1200],
            },
            index=dates,
        )


class TestYahooFinanceCrawler:
    """Yahoo Finance crawler tests."""

    def setup_method(self) -> None:
        self.crawler = YahooFinanceCrawler()
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=30)

    def test_crawler_initialization(self) -> None:
        assert self.crawler is not None
        assert self.crawler.name == "Yahoo Finance Crawler"

    def test_fetch_stock_data(self) -> None:
        with patch("financekit.crawlers.yahoo_finance.yf.Ticker", side_effect=FakeTicker):
            data = self.crawler.fetch_stock_data("AAPL", self.start_date, self.end_date)
        assert len(data) > 0
        assert all(d.symbol == "AAPL" for d in data)
        assert all(d.close > 0 for d in data)

    def test_fetch_crypto_data(self) -> None:
        with patch("financekit.crawlers.yahoo_finance.yf.Ticker", side_effect=FakeTicker):
            data = self.crawler.fetch_crypto_data("BTC-USD", self.start_date, self.end_date)
        assert len(data) > 0
        assert all(d.symbol == "BTC-USD" for d in data)
        assert all(d.market_cap == 123456789.0 for d in data)


class TestCryptoCrawler:
    """Crypto crawler tests."""

    def setup_method(self) -> None:
        self.crawler = CryptoCrawler()
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=30)

    def test_crypto_crawler_initialization(self) -> None:
        assert self.crawler is not None
        assert self.crawler.name == "Crypto Crawler"

    def test_supported_symbols(self) -> None:
        symbols = self.crawler.get_supported_symbols()
        assert "BTC" in symbols
        assert "ETH" in symbols

    def test_fetch_crypto_data(self) -> None:
        with patch("financekit.crawlers.yahoo_finance.yf.Ticker", side_effect=FakeTicker):
            data = self.crawler.fetch_crypto_data("BTC", self.start_date, self.end_date)
        assert len(data) > 0
        assert all(d.symbol == "BTC-USD" for d in data)

    def test_stock_data_not_supported(self) -> None:
        with pytest.raises(NotImplementedError):
            self.crawler.fetch_stock_data("AAPL", self.start_date, self.end_date)
