"""爬虫基类"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Any
from ..models import StockData, CryptoData


class BaseCrawler(ABC):
    """爬虫基类"""
    
    def __init__(self, name: str):
        """
        初始化爬虫
        
        Args:
            name: 爬虫名称
        """
        self.name = name
        self.session = None
    
    @abstractmethod
    def fetch_stock_data(self, symbol: str, start_date: datetime, 
                         end_date: datetime) -> List[StockData]:
        """
        获取股票数据
        
        Args:
            symbol: 股票符号
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            股票数据列表
        """
        pass
    
    @abstractmethod
    def fetch_crypto_data(self, symbol: str, start_date: datetime,
                          end_date: datetime) -> List[CryptoData]:
        """
        获取加密货币数据
        
        Args:
            symbol: 加密货币符号
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            加密货币数据列表
        """
        pass
    
    def _parse_date(self, date_str: str, format_str: str = "%Y-%m-%d") -> datetime:
        """解析日期字符串"""
        return datetime.strptime(date_str, format_str)
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"
