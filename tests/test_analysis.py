"""
单元测试 - 分析模块
"""

import pytest
from financekit import TechnicalIndicators, StatisticalAnalysis


class TestTechnicalIndicators:
    """技术指标测试"""
    
    def setup_method(self):
        """设置测试数据"""
        self.prices = [100 + i * 0.5 for i in range(50)]
    
    def test_moving_average(self):
        """测试移动平均线"""
        ma = TechnicalIndicators.moving_average(self.prices, 10)
        assert len(ma) == len(self.prices) - 10 + 1
        assert all(98 < m < 130 for m in ma)  # 合理范围
    
    def test_exponential_moving_average(self):
        """测试指数移动平均线"""
        ema = TechnicalIndicators.exponential_moving_average(self.prices, 10)
        assert len(ema) > 0
        assert all(isinstance(e, float) for e in ema)
    
    def test_rsi(self):
        """测试RSI"""
        rsi = TechnicalIndicators.rsi(self.prices, 14)
        assert len(rsi) > 0
        assert all(0 <= r <= 100 for r in rsi)
    
    def test_bollinger_bands(self):
        """测试布林线"""
        middle, upper, lower = TechnicalIndicators.bollinger_bands(self.prices, 20)
        assert len(middle) == len(upper) == len(lower)
        assert all(l <= m <= u for l, m, u in zip(lower, middle, upper))
    
    def test_macd(self):
        """测试MACD"""
        macd_line, signal_line, histogram = TechnicalIndicators.macd(self.prices)
        assert len(macd_line) > 0
        assert len(signal_line) > 0
        assert len(histogram) > 0


class TestStatisticalAnalysis:
    """统计分析测试"""
    
    def setup_method(self):
        """设置测试数据"""
        self.prices = [100 + i * 0.5 for i in range(50)]
    
    def test_calculate_returns(self):
        """测试收益率计算"""
        returns = StatisticalAnalysis.calculate_returns(self.prices)
        assert len(returns) == len(self.prices) - 1
        assert all(0.004 < r < 0.006 for r in returns)  # 恒定增长
    
    def test_calculate_volatility(self):
        """测试波动率计算"""
        volatility = StatisticalAnalysis.calculate_volatility(self.prices, 20)
        assert 0 <= volatility <= 1
    
    def test_calculate_sharpe_ratio(self):
        """测试夏普比率"""
        sharpe = StatisticalAnalysis.calculate_sharpe_ratio(self.prices)
        assert isinstance(sharpe, float)
    
    def test_calculate_max_drawdown(self):
        """测试最大回撤"""
        max_dd, start, end = StatisticalAnalysis.calculate_max_drawdown(self.prices)
        assert 0 <= max_dd <= 1
        assert isinstance(start, int)
        assert isinstance(end, int)
    
    def test_correlation_analysis(self):
        """测试相关系数"""
        prices_a = self.prices
        prices_b = [p * 1.1 for p in self.prices]  # 完全正相关
        
        corr = StatisticalAnalysis.correlation_analysis(prices_a, prices_b)
        assert -1 <= corr <= 1
        assert corr > 0.9  # 高度正相关


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
