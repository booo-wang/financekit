# FinanceKit 快速指南

欢迎使用 FinanceKit！本快速指南将帮助你快速上手。

## 📦 安装

```bash
# 开发模式安装
pip install -e .

# 或安装依赖
pip install -r requirements.txt
```

## 🚀 5分钟入门

### 第一步：获取股票数据

```python
from financekit import YahooFinanceCrawler
from datetime import datetime, timedelta

# 初始化爬虫
crawler = YahooFinanceCrawler()

# 设置时间范围
end_date = datetime.now()
start_date = end_date - timedelta(days=100)

# 获取数据
data = crawler.fetch_stock_data("AAPL", start_date, end_date)

print(f"获取了 {len(data)} 条数据")
```

### 第二步：计算技术指标

```python
from financekit import TechnicalIndicators

# 获取收盘价
closes = [d.close for d in data]

# 计算指标
sma = TechnicalIndicators.moving_average(closes, 20)
rsi = TechnicalIndicators.rsi(closes, 14)

print(f"SMA(20): {sma[-1]:.2f}")
print(f"RSI(14): {rsi[-1]:.2f}")
```

### 第三步：进行统计分析

```python
from financekit import StatisticalAnalysis

# 计算统计指标
stats = StatisticalAnalysis.calculate_statistics(data)

print(f"收益率: {stats['total_return']*100:.2f}%")
print(f"波动率: {stats['volatility']*100:.2f}%")
print(f"夏普比率: {stats['sharpe_ratio']:.2f}")
```

## 📊 常用功能

### 获取加密货币数据

```python
from financekit import CryptoCrawler

crawler = CryptoCrawler()
btc_data = crawler.fetch_crypto_data("BTC", start_date, end_date)
```

### 提取机器学习特征

```python
from financekit import FeatureExtraction

features = FeatureExtraction.extract_all_features(data)

print(features['price_features'])
print(features['volatility_features'])
print(features['momentum_features'])
```

### 使用缓存

```python
from financekit import DataCache

cache = DataCache(ttl_hours=24)

# 保存数据
cache.set("my_data", data)

# 读取缓存
cached_data = cache.get("my_data")
```

## 📚 更多资源

- **完整文档**: 查看 [README.md](README.md)
- **技术分析示例**: [examples/technical_analysis.py](examples/technical_analysis.py)
- **加密货币示例**: [examples/crypto_analysis.py](examples/crypto_analysis.py)
- **API 参考**: [README.md#-api-参考](README.md#-api-参考)

## 🆘 常见问题

### Q: 如何报告问题？
A: 请在 GitHub 上创建 Issue，包含详细的错误信息和重现步骤。

### Q: 如何贡献代码？
A: 查看 [CONTRIBUTING.md](CONTRIBUTING.md) 获取贡献指南。

### Q: 支持哪些 Python 版本？
A: 支持 Python 3.8+

## 🎯 下一步

1. 运行 `examples/basic_usage.py` 查看基本示例
2. 查看 `examples/technical_analysis.py` 学习高级用法
3. 阅读完整文档了解所有功能

祝你使用愉快！🎉
