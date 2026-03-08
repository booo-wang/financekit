"""技术指标计算模块"""
import numpy as np
from typing import List, Tuple
from ..models import StockData, CryptoData, Indicator


class TechnicalIndicators:
    """技术指标计算类"""
    
    @staticmethod
    def moving_average(prices: List[float], window: int = 20) -> List[float]:
        """
        计算简单移动平均线 (SMA)
        
        Args:
            prices: 价格列表
            window: 窗口大小
        
        Returns:
            移动平均值列表
        """
        if len(prices) < window:
            return []
        
        ma = []
        for i in range(len(prices) - window + 1):
            ma.append(np.mean(prices[i:i + window]))
        
        return ma
    
    @staticmethod
    def exponential_moving_average(prices: List[float], window: int = 20) -> List[float]:
        """
        计算指数移动平均线 (EMA)
        
        Args:
            prices: 价格列表
            window: 窗口大小
        
        Returns:
            指数移动平均值列表
        """
        if len(prices) < window:
            return []
        
        ema = [np.mean(prices[:window])]
        multiplier = 2 / (window + 1)
        
        for price in prices[window:]:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
        
        return ema
    
    @staticmethod
    def macd(prices: List[float], fast: int = 12, slow: int = 26,
             signal: int = 9) -> Tuple[List[float], List[float], List[float]]:
        """
        计算MACD (Moving Average Convergence Divergence)
        
        Args:
            prices: 价格列表
            fast: 快速EMA周期
            slow: 慢速EMA周期
            signal: 信号线周期
        
        Returns:
            (MACD线, 信号线, 柱状图)
        """
        ema_fast = TechnicalIndicators.exponential_moving_average(prices, fast)
        ema_slow = TechnicalIndicators.exponential_moving_average(prices, slow)
        
        # 对齐长度
        min_len = min(len(ema_fast), len(ema_slow))
        ema_fast = ema_fast[-min_len:]
        ema_slow = ema_slow[-min_len:]
        
        macd_line = [f - s for f, s in zip(ema_fast, ema_slow)]
        
        signal_line = TechnicalIndicators.exponential_moving_average(macd_line, signal)
        histogram = [m - s for m, s in zip(macd_line[-len(signal_line):], signal_line)]
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def rsi(prices: List[float], window: int = 14) -> List[float]:
        """
        计算相对强弱指数 (RSI)
        
        Args:
            prices: 价格列表
            window: 窗口大小
        
        Returns:
            RSI值列表 (0-100)
        """
        if len(prices) < window + 1:
            return []
        
        deltas = np.diff(prices)
        seed = deltas[:window+1]
        
        up = seed[seed >= 0].sum() / window
        down = -seed[seed < 0].sum() / window
        
        rsi = [100. if down == 0 else 100. - 100. / (1. + up / down)]
        
        for d in deltas[window+1:]:
            if d >= 0:
                up = (up * (window - 1) + d) / window
                down = (down * (window - 1)) / window
            else:
                up = (up * (window - 1)) / window
                down = (down * (window - 1) - d) / window
            
            rs = up / down if down != 0 else 0
            rsi.append(100. - 100. / (1. + rs))
        
        return rsi
    
    @staticmethod
    def bollinger_bands(prices: List[float], window: int = 20,
                        num_std: float = 2) -> Tuple[List[float], List[float], List[float]]:
        """
        计算布林线 (Bollinger Bands)
        
        Args:
            prices: 价格列表
            window: 窗口大小
            num_std: 标准差倍数
        
        Returns:
            (中线, 上线, 下线)
        """
        if len(prices) < window:
            return [], [], []
        
        middle = TechnicalIndicators.moving_average(prices, window)
        
        upper = []
        lower = []
        
        for i in range(len(prices) - window + 1):
            std = np.std(prices[i:i + window])
            upper.append(middle[i] + num_std * std)
            lower.append(middle[i] - num_std * std)
        
        return middle, upper, lower
    
    @staticmethod
    def analyze_stock(data: List[StockData]) -> dict:
        """
        分析股票数据，返回多个技术指标
        
        Args:
            data: 股票数据列表
        
        Returns:
            技术指标字典
        """
        if len(data) < 20:
            return {}
        
        closes = [d.close for d in data]
        
        indicators = {
            'sma_20': TechnicalIndicators.moving_average(closes, 20)[-1] if closes else None,
            'sma_50': TechnicalIndicators.moving_average(closes, 50)[-1] if len(closes) >= 50 else None,
            'ema_12': TechnicalIndicators.exponential_moving_average(closes, 12)[-1] if len(closes) >= 12 else None,
            'rsi_14': TechnicalIndicators.rsi(closes, 14)[-1] if len(closes) >= 15 else None,
        }
        
        macd, signal, _ = TechnicalIndicators.macd(closes)
        if macd:
            indicators['macd'] = macd[-1]
            indicators['macd_signal'] = signal[-1] if signal else None
        
        middle, upper, lower = TechnicalIndicators.bollinger_bands(closes, 20)
        if middle:
            indicators['bb_middle'] = middle[-1]
            indicators['bb_upper'] = upper[-1]
            indicators['bb_lower'] = lower[-1]
        
        return indicators
