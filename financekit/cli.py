"""Command-line entry point for FinanceKit."""

import argparse
from datetime import datetime, timedelta

from typing import Union, List

from . import __version__
from .crawlers import YahooFinanceCrawler, CryptoCrawler
from .models import StockData, CryptoData
from .analysis import TechnicalIndicators, StatisticalAnalysis


def _parse_date(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d")


def cmd_fetch(args: argparse.Namespace) -> int:
    """Fetch market data and print to stdout."""
    end = args.end or datetime.now()
    start = args.start or (end - timedelta(days=args.days))

    data: Union[List[StockData], List[CryptoData]]
    if args.crypto:
        crypto_crawler = CryptoCrawler()
        data = crypto_crawler.fetch_crypto_data(args.symbol, start, end)
    else:
        stock_crawler = YahooFinanceCrawler()
        data = stock_crawler.fetch_stock_data(args.symbol, start, end)

    if not data:
        print(f"No data found for {args.symbol}")
        return 1

    print(f"{'Date':<12} {'Open':>10} {'High':>10} {'Low':>10} {'Close':>10} {'Volume':>14}")
    print("-" * 70)
    for d in data:
        print(
            f"{d.date.strftime('%Y-%m-%d'):<12} "
            f"{d.open:>10.2f} {d.high:>10.2f} {d.low:>10.2f} {d.close:>10.2f} "
            f"{int(d.volume):>14,}"
        )

    print(f"\nTotal: {len(data)} records")
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    """Run technical analysis on a symbol."""
    end = args.end or datetime.now()
    start = args.start or (end - timedelta(days=args.days))

    crawler = YahooFinanceCrawler()
    data = crawler.fetch_stock_data(args.symbol, start, end)

    if not data:
        print(f"No data found for {args.symbol}")
        return 1

    closes = [d.close for d in data]
    highs = [d.high for d in data]
    lows = [d.low for d in data]

    print(f"=== {args.symbol} Technical Analysis ({len(data)} days) ===\n")

    # Price summary
    print(f"Latest Close: {closes[-1]:.2f}")
    print(f"Period High:  {max(highs):.2f}")
    print(f"Period Low:   {min(lows):.2f}\n")

    # Technical indicators
    indicators = TechnicalIndicators.analyze_stock(data)
    if indicators:
        print("--- Indicators ---")
        for name, value in indicators.items():
            if value is not None:
                print(f"  {name:<16} {value:>12.4f}")
        print()

    # Statistics
    stats = StatisticalAnalysis.calculate_statistics(data)
    if stats:
        print("--- Statistics ---")
        for name, value in stats.items():
            if isinstance(value, float):
                print(f"  {name:<16} {value:>12.4f}")
        print()

    return 0


def main() -> int:
    """Run the FinanceKit CLI."""
    parser = argparse.ArgumentParser(
        prog="financekit",
        description=f"FinanceKit {__version__} - Financial data and analysis CLI",
    )
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command")

    # fetch subcommand
    fetch_parser = subparsers.add_parser("fetch", help="Fetch market data")
    fetch_parser.add_argument("symbol", help="Ticker symbol (e.g. AAPL, BTC)")
    fetch_parser.add_argument("--crypto", action="store_true", help="Fetch as cryptocurrency")
    fetch_parser.add_argument("--start", type=_parse_date, help="Start date (YYYY-MM-DD)")
    fetch_parser.add_argument("--end", type=_parse_date, help="End date (YYYY-MM-DD)")
    fetch_parser.add_argument("--days", type=int, default=30, help="Number of days (default: 30)")

    # analyze subcommand
    analyze_parser = subparsers.add_parser("analyze", help="Run technical analysis")
    analyze_parser.add_argument("symbol", help="Ticker symbol (e.g. AAPL, MSFT)")
    analyze_parser.add_argument("--start", type=_parse_date, help="Start date (YYYY-MM-DD)")
    analyze_parser.add_argument("--end", type=_parse_date, help="End date (YYYY-MM-DD)")
    analyze_parser.add_argument("--days", type=int, default=90, help="Number of days (default: 90)")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "fetch":
        return cmd_fetch(args)
    elif args.command == "analyze":
        return cmd_analyze(args)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
