"""
加密货币分析示例
演示如何分析加密货币数据
"""

from datetime import datetime, timedelta
from financekit import (
    CryptoCrawler,
    TechnicalIndicators,
    StatisticalAnalysis,
    FeatureExtraction,
)


def analyze_crypto(symbol: str, days: int = 100):
    """
    加密货币分析
    
    Args:
        symbol: 加密货币符号 (BTC, ETH 等)
        days: 回溯天数
    """
    print("=" * 70)
    print(f"加密货币分析: {symbol}")
    print("=" * 70)
    
    # 获取数据
    crawler = CryptoCrawler()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    crypto_data = crawler.fetch_crypto_data(symbol, start_date, end_date)
    
    if not crypto_data:
        print(f"无法获取 {symbol} 的数据")
        return
    
    print(f"\n数据范围: {crypto_data[0].date.date()} 到 {crypto_data[-1].date.date()}")
    print(f"共 {len(crypto_data)} 条数据")
    
    # 基本信息
    print("\n" + "-" * 70)
    print("基本信息")
    print("-" * 70)
    
    latest = crypto_data[-1]
    print(f"当前价格: ${latest.close:,.2f}")
    print(f"24小时最高: ${latest.high:,.2f}")
    print(f"24小时最低: ${latest.low:,.2f}")
    print(f"成交量: ${latest.volume:,.0f}")
    if latest.market_cap:
        print(f"市值: ${latest.market_cap:,.0f}")
    
    # 价格变化
    print("\n" + "-" * 70)
    print("价格变化")
    print("-" * 70)
    
    price_change = (latest.close - crypto_data[0].close) / crypto_data[0].close
    print(f"周期收益: {price_change*100:+.2f}%")
    
    # 技术指标
    print("\n" + "-" * 70)
    print("技术指标")
    print("-" * 70)
    
    closes = [record.close for record in crypto_data]
    
    sma_20 = TechnicalIndicators.moving_average(closes, 20)
    ema_12 = TechnicalIndicators.exponential_moving_average(closes, 12)
    rsi = TechnicalIndicators.rsi(closes, 14)
    
    if sma_20:
        print(f"SMA(20): ${sma_20[-1]:,.2f}")
    if ema_12:
        print(f"EMA(12): ${ema_12[-1]:,.2f}")
    if rsi:
        print(f"RSI(14): {rsi[-1]:.2f}")
    
    # MACD
    macd_line, signal_line, histogram = TechnicalIndicators.macd(closes)
    if macd_line and histogram:
        macd_val = macd_line[-1]
        hist_val = histogram[-1]
        print(f"MACD: {macd_val:.4f} (柱状图: {hist_val:.4f})")
    
    # 波动率分析
    print("\n" + "-" * 70)
    print("波动率分析")
    print("-" * 70)
    
    volatility = StatisticalAnalysis.calculate_volatility(closes, 20)
    volatility_long = StatisticalAnalysis.calculate_volatility(closes, 50)
    
    print(f"20日波动率: {volatility*100:.2f}%")
    print(f"50日波动率: {volatility_long*100:.2f}%")
    
    if volatility > volatility_long * 1.5:
        print("⚠️  波动率大幅增加 - 高风险模式")
    else:
        print("✅ 波动率相对稳定")
    
    # 统计指标
    print("\n" + "-" * 70)
    print("性能指标")
    print("-" * 70)
    
    stats = StatisticalAnalysis.calculate_statistics(crypto_data)
    
    print(f"总收益: {stats.get('total_return', 0)*100:+.2f}%")
    print(f"最大回撤: {stats.get('max_drawdown', 0)*100:.2f}%")
    print(f"夏普比率: {stats.get('sharpe_ratio', 0):.2f}")
    
    # 特征提取
    print("\n" + "-" * 70)
    print("特征提取（用于ML）")
    print("-" * 70)
    
    features = FeatureExtraction.extract_all_features(crypto_data)
    
    print("\n价格特征:")
    for key, value in features['price_features'].items():
        print(f"  {key}: {value:.4f}")
    
    print("\n波动率特征:")
    for key, value in features['volatility_features'].items():
        print(f"  {key}: {value:.4f}")
    
    print("\n动量特征:")
    for key, value in features['momentum_features'].items():
        print(f"  {key}: {value:.4f}")
    
    # 交易建议
    print("\n" + "=" * 70)
    print("💡 交易建议")
    print("=" * 70)
    
    # 基于指标的信号
    signals = []
    
    if sma_20 and latest.close > sma_20[-1]:
        signals.append("✅ 价格在SMA(20)上方")
    elif sma_20:
        signals.append("❌ 价格在SMA(20)下方")
    
    if rsi and rsi[-1] > 70:
        signals.append("⚠️  RSI超买 - 可能回调")
    elif rsi and rsi[-1] < 30:
        signals.append("⚠️  RSI超卖 - 可能反弹")
    
    if volatility > volatility_long:
        signals.append("📈 波动率上升 - 交易机会")
    
    for signal in signals:
        print(signal)
    
    print("\n" + "=" * 70)


def main():
    # 分析主要加密货币
    cryptos = ["BTC", "ETH", "BNB"]
    
    for crypto in cryptos:
        try:
            analyze_crypto(crypto, days=100)
            print("\n")
        except Exception as e:
            print(f"分析 {crypto} 时出错: {e}\n")


if __name__ == "__main__":
    main()
