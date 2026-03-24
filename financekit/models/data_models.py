"""数据模型定义"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass
class StockData:
    """股票数据模型"""

    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: Optional[float] = None
    change_percent: Optional[float] = None

    def __post_init__(self):
        """计算额外字段"""
        if self.adjusted_close is None:
            self.adjusted_close = self.close
        if self.change_percent is None and self.open != 0:
            self.change_percent = ((self.close - self.open) / self.open) * 100


@dataclass
class CryptoData:
    """加密货币数据模型"""

    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    market_cap: Optional[float] = None
    change_percent_24h: Optional[float] = None

    def __post_init__(self):
        """计算额外字段"""
        if self.change_percent_24h is None and self.open != 0:
            self.change_percent_24h = ((self.close - self.open) / self.open) * 100


@dataclass
class Indicator:
    """技术指标模型"""

    name: str
    value: float
    description: str = ""
    signal: Optional[str] = None  # "buy", "sell", "hold"
    confidence: float = 0.0  # 0-1的置信度
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisResult:
    """分析结果模型"""

    symbol: str
    date: datetime
    indicators: Dict[str, Indicator] = field(default_factory=dict)
    summary: str = ""
    recommendation: str = ""  # "buy", "sell", "hold"
    confidence: float = 0.0
    analysis_type: str = "technical"  # "technical", "fundamental", "sentiment"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_indicator(self, name: str, indicator: Indicator):
        """添加指标"""
        self.indicators[name] = indicator

    def get_all_signals(self) -> Dict[str, str]:
        """获取所有信号"""
        return {name: ind.signal for name, ind in self.indicators.items() if ind.signal is not None}
