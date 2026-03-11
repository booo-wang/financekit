"""
FinanceKit - 金融数据爬虫和分析框架
高质量的开源金融数据获取和技术分析库
"""

__version__ = "0.2.0"
__author__ = "booo-wang"
__license__ = "MIT"

from .crawlers import (
    BaseCrawler,
    YahooFinanceCrawler,
    CryptoCrawler,
)

from .analysis import (
    TechnicalIndicators,
    StatisticalAnalysis,
    FeatureExtraction,
)

from .models import (
    StockData,
    CryptoData,
    AnalysisResult,
    Indicator,
)

from .storage import DataCache
from .utils import setup_logger, get_logger

__all__ = [
    # Crawlers
    "BaseCrawler",
    "YahooFinanceCrawler",
    "CryptoCrawler",
    
    # Analysis
    "TechnicalIndicators",
    "StatisticalAnalysis",
    "FeatureExtraction",
    
    # Models
    "StockData",
    "CryptoData",
    "AnalysisResult",
    "Indicator",
    
    # Storage
    "DataCache",
    
    # Utils
    "setup_logger",
    "get_logger",
]
