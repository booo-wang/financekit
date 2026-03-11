# FinanceKit 📊

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/booo-wang/financekit)

**FinanceKit** 是一个专业的金融数据爬虫和分析框架，提供高质量的金融数据获取和技术分析功能。

## 🎯 核心功能

### 📥 多源数据爬虫
- **股票数据**: 支持全球主要交易所的股票数据
- **加密货币**: BTC、ETH、BNB 等主流数字资产
- **灵活爬虫**: 可扩展的爬虫架构，易于添加新数据源

### 📈 技术指标分析
- **移动平均线**: SMA (简单移动平均), EMA (指数移动平均)
- **MACD**: Moving Average Convergence Divergence
- **RSI**: 相对强弱指数 (14日)
- **布林线**: Bollinger Bands (上轨、中线、下轨)

```python
from financekit import TechnicalIndicators, StockData

# 计算技术指标
sma = TechnicalIndicators.moving_average(prices, window=20)
ema = TechnicalIndicators.exponential_moving_average(prices, window=12)
rsi = TechnicalIndicators.rsi(prices, window=14)
macd, signal, histogram = TechnicalIndicators.macd(prices)
```

### 📊 统计分析
- **收益率计算**: 日收益率、总收益率
- **波动率分析**: 基于不同时间窗口的波动率计算
- **风险指标**: 
  - 夏普比率 (Sharpe Ratio)
  - 最大回撤 (Maximum Drawdown)
- **相关系数**: 多资产之间的相关性分析

```python
from financekit import StatisticalAnalysis

# 计算统计指标
stats = StatisticalAnalysis.calculate_statistics(stock_data)
sharpe = StatisticalAnalysis.calculate_sharpe_ratio(prices)
max_dd, start, end = StatisticalAnalysis.calculate_max_drawdown(prices)
correlation = StatisticalAnalysis.correlation_analysis(prices_a, prices_b)
```

### 🔧 特征工程
- **价格特征**: 价格范围、高低差、开收差异
- **波动率特征**: 多时间窗口的波动率
- **动量特征**: 短期、中期、长期动量
- **自动提取**: 一键提取所有特征用于机器学习

```python
from financekit import FeatureExtraction

# 提取所有特征
features = FeatureExtraction.extract_all_features(stock_data)
```

### 💾 智能缓存
- **自动缓存**: 避免重复爬虫请求
- **TTL机制**: 可配置的缓存过期时间
- **文件存储**: 基于文件系统的持久化缓存

## 📦 安装

### 使用pip安装（发布到PyPI后）
```bash
pip install financekit
```

### 本地开发安装
```bash
git clone https://github.com/booo-wang/financekit.git
cd financekit
pip install -e .
```

### 安装依赖
```bash
pip install -r requirements.txt
```

## 🚀 快速开始

### 1. 获取股票数据
```python
from financekit import YahooFinanceCrawler
from datetime import datetime, timedelta

# 初始化爬虫
crawler = YahooFinanceCrawler()

# 设置时间范围
end_date = datetime.now()
start_date = end_date - timedelta(days=100)

# 获取数据
stock_data = crawler.fetch_stock_data("AAPL", start_date, end_date)

print(f"获取了 {len(stock_data)} 条数据")
for record in stock_data[:3]:
    print(f"{record.date}: {record.close}")
```

### 2. 技术分析
```python
from financekit import TechnicalIndicators

# 提取收盘价
closes = [record.close for record in stock_data]

# 计算指标
sma_20 = TechnicalIndicators.moving_average(closes, 20)
rsi_14 = TechnicalIndicators.rsi(closes, 14)
bb_middle, bb_upper, bb_lower = TechnicalIndicators.bollinger_bands(closes, 20)

print(f"SMA(20): {sma_20[-1]:.2f}")
print(f"RSI(14): {rsi_14[-1]:.2f}")
print(f"Bollinger Bands: {bb_lower[-1]:.2f} - {bb_upper[-1]:.2f}")
```

### 3. 统计分析
```python
from financekit import StatisticalAnalysis

# 计算统计指标
stats = StatisticalAnalysis.calculate_statistics(stock_data)

print(f"总收益: {stats['total_return']*100:.2f}%")
print(f"波动率: {stats['volatility']*100:.2f}%")
print(f"夏普比率: {stats['sharpe_ratio']:.2f}")
print(f"最大回撤: {stats['max_drawdown']*100:.2f}%")
```

### 4. 特征提取
```python
from financekit import FeatureExtraction

# 提取特征用于机器学习
features = FeatureExtraction.extract_all_features(stock_data)

print("\\n=== 价格特征 ===")
for key, value in features['price_features'].items():
    print(f"{key}: {value:.4f}")

print("\\n=== 波动率特征 ===")
for key, value in features['volatility_features'].items():
    print(f"{key}: {value:.4f}")

print("\\n=== 动量特征 ===")
for key, value in features['momentum_features'].items():
    print(f"{key}: {value:.4f}")
```

### 5. 加密货币分析
```python
from financekit import CryptoCrawler

# 获取加密货币数据
crypto_crawler = CryptoCrawler()
btc_data = crypto_crawler.fetch_crypto_data("BTC", start_date, end_date)

print(f"BTC 数据: {len(btc_data)} 条")
```

### 6. 缓存使用
```python
from financekit import DataCache

# 创建缓存实例
cache = DataCache(ttl_hours=24)

# 保存数据
cache.set("btc_data_2024", btc_data)

# 读取缓存
cached_data = cache.get("btc_data_2024")

# 清理过期缓存
cache.clear_expired()
```

## 📚 项目结构

```
financekit/
├── financekit/
│   ├── crawlers/          # 数据爬虫模块
│   │   ├── base.py        # 爬虫基类
│   │   ├── yahoo_finance.py
│   │   └── crypto.py      # 加密货币爬虫
│   ├── analysis/          # 分析模块
│   │   ├── indicators.py  # 技术指标
│   │   ├── statistics.py  # 统计分析
│   │   └── features.py    # 特征工程
│   ├── models/            # 数据模型
│   ├── storage/           # 存储与缓存
│   ├── utils/             # 工具函数
│   └── __init__.py
├── examples/              # 使用示例
├── tests/                 # 单元测试
├── setup.py
├── requirements.txt
└── README.md
```

## 🎓 示例代码

查看 `examples/` 目录获取完整的使用示例：
- `basic_usage.py` - 基础使用示例
- `technical_analysis.py` - 技术分析示例
- `crypto_analysis.py` - 加密货币分析示例

## 🧪 单元测试

运行测试套件：
```bash
pytest tests/ -v
pytest tests/ --cov=financekit  # 生成覆盖率报告
```

## 🛠️ 开发指南

### 代码风格
- 遵循 PEP 8 标准
- 使用 `black` 格式化代码

```bash
black financekit/
flake8 financekit/
```

### 类型检查
```bash
mypy financekit/
```

### 添加新爬虫
1. 继承 `BaseCrawler` 类
2. 实现 `fetch_stock_data()` 和 `fetch_crypto_data()` 方法
3. 添加单元测试

```python
from financekit.crawlers import BaseCrawler

class MyCustomCrawler(BaseCrawler):
    def fetch_stock_data(self, symbol, start_date, end_date):
        # 实现爬虫逻辑
        pass
```

## 📊 API 参考

### YahooFinanceCrawler
- `fetch_stock_data(symbol, start_date, end_date)` - 获取股票数据
- `fetch_crypto_data(symbol, start_date, end_date)` - 获取加密货币数据

### TechnicalIndicators
- `moving_average(prices, window)` - 简单移动平均
- `exponential_moving_average(prices, window)` - 指数移动平均
- `rsi(prices, window)` - 相对强弱指数
- `macd(prices, fast, slow, signal)` - MACD
- `bollinger_bands(prices, window, num_std)` - 布林线

### StatisticalAnalysis
- `calculate_returns(prices)` - 计算收益率
- `calculate_volatility(prices, window)` - 计算波动率
- `calculate_sharpe_ratio(prices, risk_free_rate)` - 计算夏普比率
- `calculate_max_drawdown(prices)` - 计算最大回撤
- `correlation_analysis(prices_a, prices_b)` - 相关系数分析

### FeatureExtraction
- `extract_price_features(data)` - 价格特征
- `extract_volatility_features(data, window)` - 波动率特征
- `extract_momentum_features(data)` - 动量特征
- `extract_all_features(data)` - 提取所有特征

## 📝 常见问题 (FAQ)

### Q: 数据来源是什么？
A: 当前版本使用 Yahoo Finance 作为数据来源。计划支持更多数据源。

### Q: 如何获取实时数据？
A: 当前版本提供历史数据。实时数据支持在规划中。

### Q: 支持哪些市场？
A: 支持美国股市、香港股市等主要市场的股票，以及主流加密货币。

## 🤝 贡献指南

欢迎提出问题和拉取请求！

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request


## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 👤 作者

**booo-wang**
- GitHub: [@booo-wang](https://github.com/booo-wang)
- Email: christinjack_@outlook.com

## 🌟 致谢

感谢所有贡献者和使用者的支持！

## 📮 联系方式

- 问题反馈: [GitHub Issues](https://github.com/booo-wang/financekit/issues)
- 功能建议: [GitHub Issues (enhancement)](https://github.com/booo-wang/financekit/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

---

**⭐ 如果这个项目对你有帮助，请不要忘记给它一个 Star！**
