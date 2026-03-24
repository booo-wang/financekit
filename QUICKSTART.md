# FinanceKit Quickstart

```bash
pip install -e ".[dev]"
```

## 获取行情

```python
from datetime import datetime, timedelta

from financekit import YahooFinanceCrawler

end_date = datetime.now()
start_date = end_date - timedelta(days=30)

crawler = YahooFinanceCrawler()
data = crawler.fetch_stock_data("AAPL", start_date, end_date)
print(len(data))
```

## 技术分析

```python
from financekit import TechnicalIndicators

closes = [item.close for item in data]
print(TechnicalIndicators.moving_average(closes, 20)[-1])
print(TechnicalIndicators.rsi(closes, 14)[-1])
```

## 更多资源

- 项目说明：[`README.md`](README.md)
- 示例脚本：[`examples/`](examples)
