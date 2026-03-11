# FinanceKit Changelog

所有重要的变更都会记录在此。

## [0.2.0] - 2026-03-11

### 修复
- ✅ 修复 `calculate_statistics` 中 `max_drawdown` 变量名错误 (NameError)
- ✅ 修复 `validate_symbol` 不支持加密货币符号 (BTC-USD) 和国际股票符号 (AAPL.HK)

### 新增
- ✅ 添加 mypy 类型检查配置
- ✅ 添加 GitHub Actions CI 工作流 (flake8 + mypy + pytest，Python 3.8-3.11)
- ✅ 添加 GitHub Actions Release 工作流 (自动发布到 PyPI)

## [0.1.0] - 2026-03-08

### 新增
- ✅ 初始版本发布
- ✅ Yahoo Finance 数据爬虫 (股票和加密货币)
- ✅ 技术指标计算 (SMA, EMA, MACD, RSI, 布林线)
- ✅ 统计分析 (收益率、波动率、夏普比率、最大回撤)
- ✅ 特征工程 (价格、波动率、动量特征)
- ✅ 智能缓存系统
- ✅ 完整的日志系统
- ✅ 数据验证工具
- ✅ 详细的文档和示例
- ✅ 单元测试

### 修复
- ✅ 修复 `YahooFinanceCrawler` 日期迭代在跨月场景下的异常
- ✅ 修复打包入口 `financekit.cli:main` 缺失问题
- ✅ 修复测试中移动平均线断言范围错误
- ✅ 修正文档中的仓库链接与作者占位信息

### 计划中的功能
- [ ] 实时数据支持
- [ ] 更多数据源 (Binance, Coinbase, 新浪财经等)
- [ ] 情感分析
- [ ] 更多技术指标 (ATR, CCI, KDJ等)
- [ ] Web UI 仪表板
- [ ] 数据库支持 (SQLite, PostgreSQL)
- [ ] 更多国家和地区的股票数据
