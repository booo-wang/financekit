"""加密货币爬虫"""
from datetime import datetime
from typing import List

from .base import BaseCrawler
from .yahoo_finance import YahooFinanceCrawler
from ..models import StockData, CryptoData
from ..utils import setup_logger


logger = setup_logger(__name__)


class CryptoCrawler(BaseCrawler):
    """加密货币数据爬虫"""
    
    SUPPORTED_SYMBOLS = {
        "BTC": "BTC-USD",
        "ETH": "ETH-USD",
        "BNB": "BNB-USD",
        "XRP": "XRP-USD",
        "ADA": "ADA-USD",
    }
    
    def __init__(self):
        """初始化爬虫"""
        super().__init__("Crypto Crawler")
        self.yahoo_crawler = YahooFinanceCrawler()
    
    def fetch_crypto_data(self, symbol: str, start_date: datetime,
                          end_date: datetime) -> List[CryptoData]:
        """
        获取加密货币数据
        
        Args:
            symbol: 加密货币符号（如 'BTC', 'ETH'）
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            加密货币数据列表
        """
        # 转换符号
        full_symbol = self.SUPPORTED_SYMBOLS.get(symbol.upper(), f"{symbol}-USD")
        
        logger.info(f"获取加密货币数据: {symbol} ({full_symbol})")
        return self.yahoo_crawler.fetch_crypto_data(full_symbol, start_date, end_date)
    
    def fetch_stock_data(self, symbol: str, start_date: datetime,
                        end_date: datetime) -> List[StockData]:
        """
        加密货币爬虫不支持股票数据
        """
        raise NotImplementedError("CryptoCrawler不支持股票数据，请使用YahooFinanceCrawler")
    
    def get_supported_symbols(self) -> dict:
        """获取支持的加密货币列表"""
        return self.SUPPORTED_SYMBOLS.copy()
