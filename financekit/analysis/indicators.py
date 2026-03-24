"""技术指标计算模块"""

import numpy as np
from typing import List, Tuple

from ..models import StockData


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
            ma.append(float(np.mean(prices[i : i + window])))

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

        ema = [float(np.mean(prices[:window]))]
        multiplier = 2 / (window + 1)

        for price in prices[window:]:
            ema.append((price - ema[-1]) * multiplier + ema[-1])

        return ema

    @staticmethod
    def macd(
        prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9
    ) -> Tuple[List[float], List[float], List[float]]:
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
        histogram = [m - s for m, s in zip(macd_line[-len(signal_line) :], signal_line)]

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

        prices_arr = np.array(prices)
        deltas = np.diff(prices_arr)
        seed = deltas[: window + 1]

        up = float(seed[seed >= 0].sum()) / window
        down = float(-seed[seed < 0].sum()) / window

        rsi = [100.0 if down == 0 else 100.0 - 100.0 / (1.0 + up / down)]

        for d in deltas[window + 1 :]:
            if d >= 0:
                up = (up * (window - 1) + d) / window
                down = (down * (window - 1)) / window
            else:
                up = (up * (window - 1)) / window
                down = (down * (window - 1) - d) / window

            rs = up / down if down != 0 else 0
            rsi.append(100.0 - 100.0 / (1.0 + rs))

        return rsi

    @staticmethod
    def bollinger_bands(
        prices: List[float], window: int = 20, num_std: float = 2
    ) -> Tuple[List[float], List[float], List[float]]:
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

        upper: List[float] = []
        lower: List[float] = []

        for i in range(len(prices) - window + 1):
            std = float(np.std(prices[i : i + window]))
            upper.append(float(middle[i] + num_std * std))
            lower.append(float(middle[i] - num_std * std))

        return middle, upper, lower

    @staticmethod
    def atr(
        highs: List[float], lows: List[float], closes: List[float], window: int = 14
    ) -> List[float]:
        """
        计算平均真实波幅 (ATR)

        Args:
            highs: 最高价列表
            lows: 最低价列表
            closes: 收盘价列表
            window: 窗口大小

        Returns:
            ATR值列表
        """
        if len(highs) < 2 or len(highs) != len(lows) or len(highs) != len(closes):
            return []

        true_ranges: List[float] = [float(highs[0] - lows[0])]
        for i in range(1, len(highs)):
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i - 1]),
                abs(lows[i] - closes[i - 1]),
            )
            true_ranges.append(float(tr))

        if len(true_ranges) < window:
            return []

        atr_values = [float(np.mean(true_ranges[:window]))]
        for i in range(window, len(true_ranges)):
            atr_values.append(
                (atr_values[-1] * (window - 1) + true_ranges[i]) / window
            )

        return atr_values

    @staticmethod
    def cci(
        highs: List[float],
        lows: List[float],
        closes: List[float],
        window: int = 20,
    ) -> List[float]:
        """
        计算商品通道指数 (CCI)

        Args:
            highs: 最高价列表
            lows: 最低价列表
            closes: 收盘价列表
            window: 窗口大小

        Returns:
            CCI值列表
        """
        if len(highs) < window or len(highs) != len(lows) or len(highs) != len(closes):
            return []

        typical_prices = [
            (h + l + c) / 3 for h, l, c in zip(highs, lows, closes)
        ]

        cci_values: List[float] = []
        for i in range(window - 1, len(typical_prices)):
            tp_window = typical_prices[i - window + 1 : i + 1]
            tp_mean = float(np.mean(tp_window))
            mean_dev = float(np.mean([abs(tp - tp_mean) for tp in tp_window]))
            if mean_dev == 0:
                cci_values.append(0.0)
            else:
                cci_values.append((typical_prices[i] - tp_mean) / (0.015 * mean_dev))

        return cci_values

    @staticmethod
    def kdj(
        highs: List[float],
        lows: List[float],
        closes: List[float],
        k_window: int = 9,
        d_smooth: int = 3,
    ) -> Tuple[List[float], List[float], List[float]]:
        """
        计算KDJ随机指标

        Args:
            highs: 最高价列表
            lows: 最低价列表
            closes: 收盘价列表
            k_window: K值窗口 (RSV周期)
            d_smooth: D值平滑周期

        Returns:
            (K线, D线, J线)
        """
        n = len(highs)
        if n < k_window or n != len(lows) or n != len(closes):
            return [], [], []

        rsv_list: List[float] = []
        for i in range(k_window - 1, n):
            high_n = max(highs[i - k_window + 1 : i + 1])
            low_n = min(lows[i - k_window + 1 : i + 1])
            if high_n == low_n:
                rsv_list.append(50.0)
            else:
                rsv_list.append((closes[i] - low_n) / (high_n - low_n) * 100)

        k_values: List[float] = [50.0]
        d_values: List[float] = [50.0]
        for rsv in rsv_list:
            k = (2 / d_smooth) * rsv + (1 - 2 / d_smooth) * k_values[-1]
            d = (2 / d_smooth) * k + (1 - 2 / d_smooth) * d_values[-1]
            k_values.append(k)
            d_values.append(d)

        # 去掉初始种子值
        k_values = k_values[1:]
        d_values = d_values[1:]
        j_values = [3 * k - 2 * d for k, d in zip(k_values, d_values)]

        return k_values, d_values, j_values

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
            "sma_20": TechnicalIndicators.moving_average(closes, 20)[-1] if closes else None,
            "sma_50": TechnicalIndicators.moving_average(closes, 50)[-1] if len(closes) >= 50 else None,
            "ema_12": TechnicalIndicators.exponential_moving_average(closes, 12)[-1] if len(closes) >= 12 else None,
            "rsi_14": TechnicalIndicators.rsi(closes, 14)[-1] if len(closes) >= 15 else None,
        }

        macd, signal, _ = TechnicalIndicators.macd(closes)
        if macd:
            indicators["macd"] = macd[-1]
            indicators["macd_signal"] = signal[-1] if signal else None

        middle, upper, lower = TechnicalIndicators.bollinger_bands(closes, 20)
        if middle:
            indicators["bb_middle"] = middle[-1]
            indicators["bb_upper"] = upper[-1]
            indicators["bb_lower"] = lower[-1]

        highs = [d.high for d in data]
        lows = [d.low for d in data]

        atr_vals = TechnicalIndicators.atr(highs, lows, closes, 14)
        if atr_vals:
            indicators["atr_14"] = atr_vals[-1]

        cci_vals = TechnicalIndicators.cci(highs, lows, closes, 20)
        if cci_vals:
            indicators["cci_20"] = cci_vals[-1]

        k, d, j = TechnicalIndicators.kdj(highs, lows, closes)
        if k:
            indicators["kdj_k"] = k[-1]
            indicators["kdj_d"] = d[-1]
            indicators["kdj_j"] = j[-1]

        return indicators
