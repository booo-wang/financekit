# FinanceKit

[![CI](https://github.com/booo-wang/financekit/actions/workflows/ci.yml/badge.svg)](https://github.com/booo-wang/financekit/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

FinanceKit 是一个专业的金融数据采集与分析框架，支持股票和加密货币的实时行情获取、技术指标计算和统计分析。

## 功能特性

- **行情数据采集** — 通过 Yahoo Finance 获取股票和加密货币的历史行情数据
- **技术指标分析** — SMA、EMA、MACD、RSI、布林带、ATR、CCI、KDJ
- **统计分析** — 收益率、波动率、夏普比率、最大回撤
- **特征工程** — 为机器学习提供价格、波动率、动量特征提取
- **智能缓存** — 基于文件系统的 TTL 缓存，避免重复请求
- **命令行工具** — `fetch` 和 `analyze` 子命令，开箱即用

## 快速开始

### 安装

```bash
pip install -e ".[dev]"
```

### 命令行使用

```bash
# 获取苹果近 5 天行情
financekit fetch AAPL --days 5

# 获取比特币行情
financekit fetch BTC --crypto --days 30

# 技术分析
financekit analyze AAPL --days 90
```

### Python API

```python
from datetime import datetime, timedelta
from financekit import YahooFinanceCrawler, TechnicalIndicators

# 获取行情数据
crawler = YahooFinanceCrawler()
end = datetime.now()
start = end - timedelta(days=30)
data = crawler.fetch_stock_data("AAPL", start, end)

# 计算技术指标
closes = [d.close for d in data]
sma = TechnicalIndicators.moving_average(closes, 20)
rsi = TechnicalIndicators.rsi(closes, 14)
macd_line, signal_line, histogram = TechnicalIndicators.macd(closes)
```

更多用法参见 [examples/](examples/) 目录。

## 项目结构

```
financekit/          Python 包源码
  crawlers/          数据爬虫（Yahoo Finance、加密货币）
  analysis/          技术指标、统计分析、特征工程
  models/            数据模型（StockData、CryptoData 等）
  storage/           文件缓存
  utils/             日志、数据校验
tests/               单元测试
examples/            示例脚本
```

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v --cov=financekit

# 类型检查
mypy financekit/

# 代码风格检查
flake8 financekit/ --max-line-length=120 --extend-ignore=E203
```

## License

[MIT](LICENSE)
