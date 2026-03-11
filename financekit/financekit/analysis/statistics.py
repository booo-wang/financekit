"""统计分析模块"""

import numpy as np
from typing import List, Dict, Tuple
from ..models import StockData


class StatisticalAnalysis:
    """统计分析类"""

    @staticmethod
    def calculate_returns(prices: List[float]) -> List[float]:
        """
        计算收益率

        Args:
            prices: 价格列表

        Returns:
            收益率列表
        """
        if len(prices) < 2:
            return []

        returns = []
        for i in range(1, len(prices)):
            ret = (prices[i] - prices[i - 1]) / prices[i - 1]
            returns.append(ret)

        return returns

    @staticmethod
    def calculate_volatility(prices: List[float], window: int = 20) -> float:
        """
        计算波动率

        Args:
            prices: 价格列表
            window: 窗口大小

        Returns:
            波动率
        """
        returns = StatisticalAnalysis.calculate_returns(prices[-window:])
        if len(returns) < 2:
            return 0.0

        return float(np.std(returns))

    @staticmethod
    def calculate_sharpe_ratio(prices: List[float], risk_free_rate: float = 0.02) -> float:
        """
        计算夏普比率

        Args:
            prices: 价格列表
            risk_free_rate: 无风险利率

        Returns:
            夏普比率
        """
        returns = StatisticalAnalysis.calculate_returns(prices)
        if len(returns) < 2:
            return 0.0

        avg_return = np.mean(returns)
        volatility = np.std(returns)

        if volatility == 0:
            return 0.0

        return (avg_return - risk_free_rate / 252) / volatility * np.sqrt(252)

    @staticmethod
    def calculate_max_drawdown(prices: List[float]) -> Tuple[float, int, int]:
        """
        计算最大回撤

        Args:
            prices: 价格列表

        Returns:
            (最大回撤, 开始位置, 结束位置)
        """
        if len(prices) < 2:
            return 0.0, 0, 0

        max_price = prices[0]
        max_drawdown = 0.0
        start_idx = 0
        end_idx = 0
        current_start = 0

        for i in range(1, len(prices)):
            if prices[i] > max_price:
                max_price = prices[i]
                current_start = i

            drawdown = (max_price - prices[i]) / max_price
            if drawdown > max_drawdown:
                max_drawdown = drawdown
                start_idx = current_start
                end_idx = i

        return max_drawdown, start_idx, end_idx

    @staticmethod
    def calculate_statistics(data: List[StockData]) -> Dict[str, float]:
        """
        计算统计指标

        Args:
            data: 股票数据列表

        Returns:
            统计指标字典
        """
        if len(data) < 2:
            return {}

        closes = [d.close for d in data]

        returns = StatisticalAnalysis.calculate_returns(closes)
        volatility = StatisticalAnalysis.calculate_volatility(closes)
        sharpe = StatisticalAnalysis.calculate_sharpe_ratio(closes)
        max_dd, start, end = StatisticalAnalysis.calculate_max_drawdown(closes)

        total_return = (closes[-1] - closes[0]) / closes[0]

        stats = {
            "total_return": float(total_return),
            "avg_daily_return": float(np.mean(returns)) if returns else 0.0,
            "volatility": float(volatility),
            "sharpe_ratio": float(sharpe),
            "max_drawdown": float(max_dd),
            "min_price": float(np.min(closes)),
            "max_price": float(np.max(closes)),
            "avg_price": float(np.mean(closes)),
        }

        return stats

    @staticmethod
    def correlation_analysis(prices_a: List[float], prices_b: List[float]) -> float:
        """
        计算两个价格序列的相关系数

        Args:
            prices_a: 价格序列A
            prices_b: 价格序列B

        Returns:
            相关系数 (-1 到 1)
        """
        if len(prices_a) != len(prices_b) or len(prices_a) < 2:
            return 0.0

        returns_a = StatisticalAnalysis.calculate_returns(prices_a)
        returns_b = StatisticalAnalysis.calculate_returns(prices_b)

        if len(returns_a) < 2 or len(returns_b) < 2:
            return 0.0

        return float(np.corrcoef(returns_a, returns_b)[0, 1])
