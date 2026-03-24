"""
单元测试 - 爬虫模块
"""

import pytest
from datetime import datetime, timedelta
from financekit import YahooFinanceCrawler, CryptoCrawler


class TestYahooFinanceCrawler:
    """Yahoo Finance爬虫测试"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.crawler = YahooFinanceCrawler()
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=30)
    
    def test_crawler_initialization(self):
        """测试爬虫初始化"""
        assert self.crawler is not None
        assert self.crawler.name == "Yahoo Finance Crawler"
    
    def test_fetch_stock_data(self):
        """测试获取股票数据"""
        data = self.crawler.fetch_stock_data("AAPL", self.start_date, self.end_date)
        assert len(data) > 0
        assert all(d.symbol == "AAPL" for d in data)
        assert all(d.close > 0 for d in data)
    
    def test_fetch_crypto_data(self):
        """测试获取加密货币数据"""
        data = self.crawler.fetch_crypto_data("BTC-USD", self.start_date, self.end_date)
        assert len(data) > 0
        assert all(d.symbol == "BTC-USD" for d in data)


class TestCryptoCrawler:
    """加密货币爬虫测试"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.crawler = CryptoCrawler()
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=30)
    
    def test_crypto_crawler_initialization(self):
        """测试爬虫初始化"""
        assert self.crawler is not None
        assert self.crawler.name == "Crypto Crawler"
    
    def test_supported_symbols(self):
        """测试支持的加密货币"""
        symbols = self.crawler.get_supported_symbols()
        assert "BTC" in symbols
        assert "ETH" in symbols
    
    def test_fetch_crypto_data(self):
        """测试获取加密货币数据"""
        data = self.crawler.fetch_crypto_data("BTC", self.start_date, self.end_date)
        assert len(data) > 0
    
    def test_stock_data_not_supported(self):
        """测试股票数据不支持"""
        with pytest.raises(NotImplementedError):
            self.crawler.fetch_stock_data("AAPL", self.start_date, self.end_date)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
