"""
技术分析示例
演示更复杂的技术分析和信号生成
"""

from datetime import datetime, timedelta
from financekit import (
    YahooFinanceCrawler,
    TechnicalIndicators,
    StatisticalAnalysis,
    AnalysisResult,
    Indicator,
)


def analyze_stock(symbol: str, days: int = 100):
    """
    完整的股票技术分析
    
    Args:
        symbol: 股票符号
        days: 回溯天数
    """
    print("=" * 70)
    print(f"技术分析: {symbol}")
    print("=" * 70)
    
    # 获取数据
    crawler = YahooFinanceCrawler()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    stock_data = crawler.fetch_stock_data(symbol, start_date, end_date)
    
    if not stock_data:
        print(f"无法获取 {symbol} 的数据")
        return
    
    print(f"\n数据范围: {stock_data[0].date.date()} 到 {stock_data[-1].date.date()}")
    print(f"共 {len(stock_data)} 个交易日")
    
    closes = [record.close for record in stock_data]
    
    # 创建分析结果
    analysis = AnalysisResult(
        symbol=symbol,
        date=datetime.now(),
        analysis_type="technical"
    )
    
    # 1. 移动平均线分析
    print("\n" + "-" * 70)
    print("1️⃣  移动平均线分析")
    print("-" * 70)
    
    sma_20 = TechnicalIndicators.moving_average(closes, 20)
    sma_50 = TechnicalIndicators.moving_average(closes, 50)
    ema_12 = TechnicalIndicators.exponential_moving_average(closes, 12)
    
    last_close = closes[-1]
    
    print(f"当前价格: ${last_close:.2f}")
    print(f"SMA(20): ${sma_20[-1]:.2f}" if sma_20 else "SMA(20): N/A")
    print(f"SMA(50): ${sma_50[-1]:.2f}" if sma_50 else "SMA(50): N/A")
    print(f"EMA(12): ${ema_12[-1]:.2f}" if ema_12 else "EMA(12): N/A")
    
    # 价格vs移动平均线
    if sma_20:
        if last_close > sma_20[-1]:
            print(f"✅ 价格在SMA(20)上方 (+{(last_close/sma_20[-1]-1)*100:.2f}%)")
        else:
            print(f"❌ 价格在SMA(20)下方 ({(last_close/sma_20[-1]-1)*100:.2f}%)")
    
    # MA 金叉死叉
    if sma_20 and sma_50 and len(sma_20) > 1 and len(sma_50) > 1:
        prev_signal = sma_20[-2] > sma_50[-2]
        curr_signal = sma_20[-1] > sma_50[-1]
        
        if curr_signal != prev_signal:
            if curr_signal:
                print("🔼 出现金叉信号 (SMA20 上穿 SMA50) - 看涨")
                analysis.add_indicator(
                    "ma_crossover",
                    Indicator(name="MA金叉", value=1.0, signal="buy", confidence=0.7)
                )
            else:
                print("🔽 出现死叉信号 (SMA20 下穿 SMA50) - 看跌")
                analysis.add_indicator(
                    "ma_crossover",
                    Indicator(name="MA死叉", value=0.0, signal="sell", confidence=0.7)
                )
    
    # 2. MACD分析
    print("\n" + "-" * 70)
    print("2️⃣  MACD分析")
    print("-" * 70)
    
    macd_line, signal_line, histogram = TechnicalIndicators.macd(closes)
    
    if macd_line and signal_line:
        print(f"MACD: {macd_line[-1]:.4f}")
        print(f"信号线: {signal_line[-1]:.4f}")
        print(f"柱状图: {histogram[-1]:.4f}")
        
        # MACD 信号
        if len(histogram) > 1:
            prev_hist = histogram[-2]
            curr_hist = histogram[-1]
            
            if curr_hist > 0 and prev_hist <= 0:
                print("🔼 MACD 柱状图转正 - 看涨")
                analysis.add_indicator(
                    "macd",
                    Indicator(name="MACD", value=curr_hist, signal="buy", confidence=0.65)
                )
            elif curr_hist < 0 and prev_hist >= 0:
                print("🔽 MACD 柱状图转负 - 看跌")
                analysis.add_indicator(
                    "macd",
                    Indicator(name="MACD", value=curr_hist, signal="sell", confidence=0.65)
                )
            else:
                signal = "buy" if curr_hist > 0 else "sell"
                print(f"MACD 柱状图维持 {signal}")
    
    # 3. RSI分析
    print("\n" + "-" * 70)
    print("3️⃣  相对强弱指数 (RSI)")
    print("-" * 70)
    
    rsi = TechnicalIndicators.rsi(closes, 14)
    
    if rsi:
        rsi_value = rsi[-1]
        print(f"RSI(14): {rsi_value:.2f}")
        
        if rsi_value > 70:
            print(f"⚠️  超买区域 (RSI > 70) - 可能要调整")
            analysis.add_indicator(
                "rsi",
                Indicator(name="RSI", value=rsi_value, signal="sell", confidence=0.6)
            )
        elif rsi_value < 30:
            print(f"⚠️  超卖区域 (RSI < 30) - 可能反弹")
            analysis.add_indicator(
                "rsi",
                Indicator(name="RSI", value=rsi_value, signal="buy", confidence=0.6)
            )
        else:
            status = "上升" if rsi_value > 50 else "下降"
            print(f"✅ 正常范围 (30-70) - 动量{status}")
    
    # 4. 布林线分析
    print("\n" + "-" * 70)
    print("4️⃣  布林线分析")
    print("-" * 70)
    
    bb_middle, bb_upper, bb_lower = TechnicalIndicators.bollinger_bands(closes, 20)
    
    if bb_middle and bb_upper and bb_lower:
        print(f"布林线上轨: ${bb_upper[-1]:.2f}")
        print(f"布林线中线: ${bb_middle[-1]:.2f}")
        print(f"布林线下轨: ${bb_lower[-1]:.2f}")
        
        if last_close >= bb_upper[-1]:
            print(f"⚠️  价格触及上轨 - 可能过热")
        elif last_close <= bb_lower[-1]:
            print(f"⚠️  价格触及下轨 - 可能过冷")
        else:
            position = (last_close - bb_lower[-1]) / (bb_upper[-1] - bb_lower[-1])
            print(f"✅ 价格在布林线内 ({position*100:.1f}%)")
    
    # 5. 波动率分析
    print("\n" + "-" * 70)
    print("5️⃣  波动率分析")
    print("-" * 70)
    
    volatility = StatisticalAnalysis.calculate_volatility(closes, 20)
    volatility_50 = StatisticalAnalysis.calculate_volatility(closes, 50)
    
    print(f"20日波动率: {volatility*100:.2f}%")
    print(f"50日波动率: {volatility_50*100:.2f}%")
    
    if volatility > volatility_50 * 1.2:
        print("⚠️  波动率升高 - 市场风险增加")
    else:
        print("✅ 波动率稳定")
    
    # 6. 统计指标
    print("\n" + "-" * 70)
    print("6️⃣  统计指标")
    print("-" * 70)
    
    stats = StatisticalAnalysis.calculate_statistics(stock_data)
    
    print(f"收益率: {stats.get('total_return', 0)*100:.2f}%")
    print(f"最大回撤: {stats.get('max_drawdown', 0)*100:.2f}%")
    print(f"夏普比率: {stats.get('sharpe_ratio', 0):.2f}")
    
    # 7. 综合信号
    print("\n" + "=" * 70)
    print("🎯 综合信号")
    print("=" * 70)
    
    signals = analysis.get_all_signals()
    buy_signals = sum(1 for s in signals.values() if s == "buy")
    sell_signals = sum(1 for s in signals.values() if s == "sell")
    
    print(f"买入信号: {buy_signals}")
    print(f"卖出信号: {sell_signals}")
    
    if buy_signals > sell_signals:
        print("\n✅ 综合信号: 看涨")
        analysis.recommendation = "buy"
    elif sell_signals > buy_signals:
        print("\n❌ 综合信号: 看跌")
        analysis.recommendation = "sell"
    else:
        print("\n➡️ 综合信号: 观望")
        analysis.recommendation = "hold"
    
    print("\n" + "=" * 70)
    return analysis


def main():
    # 分析多个股票
    symbols = ["AAPL", "MSFT", "GOOGL"]
    
    results = []
    for symbol in symbols:
        try:
            result = analyze_stock(symbol, days=100)
            results.append(result)
            print("\n")
        except Exception as e:
            print(f"分析 {symbol} 时出错: {e}\n")
    
    print("\n" + "=" * 70)
    print("📊 分析汇总")
    print("=" * 70)
    for result in results:
        if result:
            print(f"{result.symbol}: {result.recommendation.upper()}")


if __name__ == "__main__":
    main()
