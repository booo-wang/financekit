"""Unit tests for the command-line interface."""

from datetime import datetime, timedelta
from typing import List
from unittest.mock import patch

import pytest

from financekit import StockData
from financekit.cli import main


def make_stock_data(days: int = 5) -> List[StockData]:
    """Return a deterministic slice of market data for CLI tests."""
    base = datetime(2026, 3, 1)
    return [
        StockData(
            symbol="AAPL",
            date=base + timedelta(days=offset),
            open=100 + offset,
            high=101 + offset,
            low=99 + offset,
            close=100.5 + offset,
            volume=1_000 + offset * 10,
        )
        for offset in range(days)
    ]


class TestCLI:
    """CLI tests."""

    def test_version(self, capsys) -> None:
        with pytest.raises(SystemExit) as exc:
            with patch("sys.argv", ["financekit", "-V"]):
                main()
        assert exc.value.code == 0
        output = capsys.readouterr().out
        assert "0.3.0" in output

    def test_no_args_shows_help(self, capsys) -> None:
        with patch("sys.argv", ["financekit"]):
            ret = main()
        assert ret == 0
        output = capsys.readouterr().out
        assert "fetch" in output
        assert "analyze" in output

    def test_fetch_stock(self, capsys) -> None:
        with patch("financekit.cli.YahooFinanceCrawler.fetch_stock_data", return_value=make_stock_data()):
            with patch("sys.argv", ["financekit", "fetch", "AAPL", "--days", "5"]):
                ret = main()
        assert ret == 0
        output = capsys.readouterr().out
        assert "Date" in output
        assert "Total: 5 records" in output

    def test_fetch_invalid_symbol(self, capsys) -> None:
        with patch("financekit.cli.YahooFinanceCrawler.fetch_stock_data", return_value=[]):
            with patch("sys.argv", ["financekit", "fetch", "ZZZZZZZZZZ", "--days", "5"]):
                ret = main()
        assert ret == 1

    def test_analyze(self, capsys) -> None:
        with patch("financekit.cli.YahooFinanceCrawler.fetch_stock_data", return_value=make_stock_data(60)):
            with patch("sys.argv", ["financekit", "analyze", "AAPL", "--days", "60"]):
                ret = main()
        assert ret == 0
        output = capsys.readouterr().out
        assert "Technical Analysis" in output
