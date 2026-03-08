"""特征工程模块"""
import numpy as np
from typing import List, Dict
from ..models import StockData, CryptoData


class FeatureExtraction:
    """特征提取类"""
    
    @staticmethod
    def extract_price_features(data: List[StockData]) -> Dict[str, float]:
        """
        提取价格特征
        
        Args:
            data: 股票数据列表
        
        Returns:
            特征字典
        """
        if len(data) < 1:
            return {}
        
        closes = [d.close for d in data]
        opens = [d.open for d in data]
        highs = [d.high for d in data]
        lows = [d.low for d in data]
        volumes = [d.volume for d in data]
        
        # 价格范围
        price_range = max(closes) - min(closes)
        
        # 高低差平均值
        hl_avg = np.mean([h - l for h, l in zip(highs, lows)])
        
        # 开盘价与收盘价的差异
        oc_avg = np.mean([abs(o - c) for o, c in zip(opens, closes)])
        
        # 成交量特征
        avg_volume = np.mean(volumes)
        volume_std = np.std(volumes)
        
        features = {
            'price_range': float(price_range),
            'hl_average': float(hl_avg),
            'oc_average': float(oc_avg),
            'avg_volume': float(avg_volume),
            'volume_std': float(volume_std),
            'volume_volatility': float(volume_std / avg_volume) if avg_volume > 0 else 0.0,
            'close_trend': float(closes[-1] - closes[0]) if len(closes) > 1 else 0.0,
        }
        
        return features
    
    @staticmethod
    def extract_volatility_features(data: List[StockData], window: int = 20) -> Dict[str, float]:
        """
        提取波动率特征
        
        Args:
            data: 股票数据列表
            window: 窗口大小
        
        Returns:
            波动率特征字典
        """
        if len(data) < window:
            return {}
        
        closes = [d.close for d in data]
        
        # 计算收益率
        returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))]
        
        # 不同窗口的波动率
        volatility_features = {}
        
        for w in [10, 20, 50]:
            if len(returns) >= w:
                vol = np.std(returns[-w:])
                volatility_features[f'volatility_{w}d'] = float(vol)
        
        return volatility_features
    
    @staticmethod
    def extract_momentum_features(data: List[StockData]) -> Dict[str, float]:
        """
        提取动量特征
        
        Args:
            data: 股票数据列表
        
        Returns:
            动量特征字典
        """
        if len(data) < 10:
            return {}
        
        closes = [d.close for d in data]
        
        # 短期动量 (5日 vs 10日)
        short_momentum = (closes[-1] - closes[-5]) / closes[-5]
        
        # 中期动量 (10日 vs 20日)
        mid_momentum = (closes[-1] - closes[-10]) / closes[-10]
        
        # 长期动量 (20日 vs 50日)
        long_momentum = None
        if len(closes) >= 50:
            long_momentum = (closes[-1] - closes[-20]) / closes[-20]
        
        features = {
            'short_momentum': float(short_momentum),
            'mid_momentum': float(mid_momentum),
        }
        
        if long_momentum is not None:
            features['long_momentum'] = float(long_momentum)
        
        return features
    
    @staticmethod
    def extract_all_features(data: List[StockData]) -> Dict[str, Dict[str, float]]:
        """
        提取所有特征
        
        Args:
            data: 股票数据列表
        
        Returns:
            包含所有特征的字典
        """
        features = {
            'price_features': FeatureExtraction.extract_price_features(data),
            'volatility_features': FeatureExtraction.extract_volatility_features(data),
            'momentum_features': FeatureExtraction.extract_momentum_features(data),
        }
        
        return features
