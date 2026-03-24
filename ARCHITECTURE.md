# FinanceKit 架构说明

本文档描述 FinanceKit 的整体架构设计。

## 🏗️ 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                    用户应用层                             │
│  (examples/, 用户代码)                                    │
└────────────────────┬────────────────────────────────────┘
                     │
     ┌───────────────┼───────────────┐
     │               │               │
┌────▼─────────┐ ┌──▼────────────┐ ┌─▼────────────────┐
│   爬虫模块    │ │    分析模块     │ │   存储和工具      │
│  (crawlers)  │ │  (analysis)    │ │  (storage/utils) │
└────┬─────────┘ └──┬────────────┘ └─┬────────────────┘
     │              │                 │
     └──────────────┼─────────────────┘
                    │
              ┌─────▼──────┐
              │  数据模型   │
              │  (models)  │
              └────────────┘
```

## 📦 模块说明

### 1. 爬虫模块 (crawlers/)

负责从不同数据源获取金融数据。

**类**: 
- `BaseCrawler`: 所有爬虫的基类
- `YahooFinanceCrawler`: Yahoo Finance 数据爬虫
- `CryptoCrawler`: 加密货币数据爬虫

**设计模式**: 策略模式 + 模板方法

```python
class BaseCrawler(ABC):
    @abstractmethod
    def fetch_stock_data(...): pass
    
    @abstractmethod
    def fetch_crypto_data(...): pass
```

**扩展方法**: 继承 `BaseCrawler` 并实现抽象方法

### 2. 分析模块 (analysis/)

提供金融数据分析功能。

**子模块**:
- `indicators.py`: 技术指标计算
- `statistics.py`: 统计分析
- `features.py`: 特征工程

**技术指标**:
- SMA (简单移动平均)
- EMA (指数移动平均)
- MACD (动量指示器)
- RSI (相对强弱指数)
- 布林线 (Bollinger Bands)

### 3. 数据模型 (models/)

定义所有数据结构。

**数据类**:
- `StockData`: 股票数据
- `CryptoData`: 加密货币数据
- `Indicator`: 技术指标
- `AnalysisResult`: 分析结果

使用 dataclass 确保类型安全和易于序列化。

### 4. 存储和缓存 (storage/)

提供数据持久化和缓存功能。

**功能**:
- 文件系统缓存
- TTL 过期管理
- JSON 序列化

```python
cache = DataCache(ttl_hours=24)
cache.set("key", data)
data = cache.get("key")
```

### 5. 工具模块 (utils/)

提供日志、验证等通用功能。

**子模块**:
- `logger.py`: 日志配置
- `validators.py`: 数据验证

## 🔄 数据流

```
1. 初始化爬虫
   └─> 创建 Crawler 实例

2. 获取数据
   └─> crawler.fetch_stock_data(symbol, start, end)
   └─> 返回 List[StockData]

3. 分析数据
   └─> TechnicalIndicators.calculate(data)
   └─> StatisticalAnalysis.calculate(data)
   └─> FeatureExtraction.extract(data)

4. 缓存结果
   └─> cache.set(key, result)

5. 返回给用户
   └─> analysis_result
```

## 🎯 设计原则

### 1. 单一职责原则
- 每个类只负责一个功能
- 爬虫只负责数据获取
- 分析器只负责数据分析

### 2. 开闭原则
- 对扩展开放（易于添加新爬虫、新指标）
- 对修改关闭（不需要修改现有代码）

### 3. 依赖倒置原则
- 依赖抽象 (`BaseCrawler`)
- 不依赖具体实现

### 4. 类型安全
- 使用 dataclass 和类型注解
- 便于调试和自动补全

## 🔧 扩展指南

### 添加新爬虫

```python
from financekit.crawlers import BaseCrawler
from financekit.models import StockData

class MyNewCrawler(BaseCrawler):
    def __init__(self):
        super().__init__("My Crawler")
    
    def fetch_stock_data(self, symbol, start, end):
        # 实现数据获取逻辑
        pass
    
    def fetch_crypto_data(self, symbol, start, end):
        # 实现加密货币数据获取逻辑
        pass
```

### 添加新指标

```python
class TechnicalIndicators:
    @staticmethod
    def my_new_indicator(prices: List[float], **kwargs) -> List[float]:
        """计算新指标"""
        # 实现指标计算
        pass
```

## 📊 性能考虑

1. **缓存**:
   - 使用文件系统缓存避免重复爬虫
   - 可配置 TTL

2. **数据处理**:
   - 使用 NumPy 进行高效数组操作
   - 避免重复计算

3. **内存管理**:
   - dataclass 具有低内存开销
   - 支持流式处理大数据量

## 🧪 测试策略

1. **单元测试**:
   - 每个模块单独测试
   - Mock 外部依赖

2. **集成测试**:
   - 测试模块之间的交互
   - 测试完整的数据流

3. **性能测试**:
   - 测试大数据量性能
   - 测试缓存效率

## 📈 未来改进

1. 异步爬虫支持
2. 实时数据流
3. 数据库后端
4. Web API 服务
5. 前端仪表板
