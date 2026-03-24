"""
基础使用示例
演示如何使用 FinanceKit 获取数据并进行基本分析
"""

from datetime import datetime, timedelta
from financekit import (
    YahooFinanceCrawler,
    TechnicalIndicators,
    StatisticalAnalysis,
)


def main():
    print("=" * 60)
    print("FinanceKit 基础使用示例")
    print("=" * 60)
    
    # 1. 初始化爬虫
    print("\n[1] 初始化爬虫")
    crawler = YahooFinanceCrawler()
    print(f"爬虫: {crawler}")
    
    # 2. 设置时间范围
    print("\n[2] 设置时间范围")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=100)
    print(f"时间范围: {start_date.date()} 到 {end_date.date()}")
    
    # 3. 获取股票数据
    print("\n[3] 获取股票数据 (AAPL)")
    stock_data = crawler.fetch_stock_data("AAPL", start_date, end_date)
    print(f"获取了 {len(stock_data)} 条数据")
    
    # 显示最近5条数据
    print("\n最近5条数据:")
    for record in stock_data[-5:]:
        print(f"  {record.date.date()}: Open={record.open:.2f}, "
              f"Close={record.close:.2f}, Vol={record.volume:,}")
    
    # 4. 技术指标分析
    print("\n[4] 技术指标分析")
    closes = [record.close for record in stock_data]
    
    # 计算不同的技术指标
    sma_20 = TechnicalIndicators.moving_average(closes, 20)
    sma_50 = TechnicalIndicators.moving_average(closes, 50)
    ema_12 = TechnicalIndicators.exponential_moving_average(closes, 12)
    rsi_14 = TechnicalIndicators.rsi(closes, 14)
    
    print(f"SMA(20): {sma_20[-1]:.2f}" if sma_20 else "SMA(20): N/A")
    print(f"SMA(50): {sma_50[-1]:.2f}" if sma_50 else "SMA(50): N/A")
    print(f"EMA(12): {ema_12[-1]:.2f}" if ema_12 else "EMA(12): N/A")
    print(f"RSI(14): {rsi_14[-1]:.2f}" if rsi_14 else "RSI(14): N/A")
    
    # 5. 布林线计算
    print("\n[5] 布林线分析")
    bb_middle, bb_upper, bb_lower = TechnicalIndicators.bollinger_bands(closes, 20)
    if bb_middle:
        print(f"下轨: {bb_lower[-1]:.2f}")
        print(f"中线: {bb_middle[-1]:.2f}")
        print(f"上轨: {bb_upper[-1]:.2f}")
    
    # 6. MACD分析
    print("\n[6] MACD分析")
    macd_line, signal_line, histogram = TechnicalIndicators.macd(closes)
    if macd_line:
        print(f"MACD线: {macd_line[-1]:.4f}")
        print(f"信号线: {signal_line[-1]:.4f}" if signal_line else "信号线: N/A")
        print(f"柱状图: {histogram[-1]:.4f}" if histogram else "柱状图: N/A")
    
    # 7. 统计分析
    print("\n[7] 统计分析")
    stats = StatisticalAnalysis.calculate_statistics(stock_data)
    
    print(f"总收益: {stats.get('total_return', 0)*100:.2f}%")
    print(f"日均收益: {stats.get('avg_daily_return', 0)*100:.4f}%")
    print(f"波动率: {stats.get('volatility', 0)*100:.2f}%")
    print(f"夏普比率: {stats.get('sharpe_ratio', 0):.2f}")
    print(f"最大回撤: {stats.get('max_drawdown', 0)*100:.2f}%")
    
    # 8. 价格统计
    print("\n[8] 价格统计")
    print(f"最高价: {stats.get('max_price', 0):.2f}")
    print(f"最低价: {stats.get('min_price', 0):.2f}")
    print(f"平均价: {stats.get('avg_price', 0):.2f}")
    
    # 9. 交易信号生成
    print("\n[9] 简单交易信号")
    if sma_20 and sma_50:
        if sma_20[-1] > sma_50[-1]:
            signal = "🔼 买入信号 (SMA20 > SMA50)"
        else:
            signal = "🔽 卖出信号 (SMA20 < SMA50)"
        print(signal)
    
    if rsi_14:
        rsi_value = rsi_14[-1]
        if rsi_value > 70:
            rsi_signal = "⚠️  超买 (RSI > 70)"
        elif rsi_value < 30:
            rsi_signal = "⚠️  超卖 (RSI < 30)"
        else:
            rsi_signal = "✅ 正常 (30 < RSI < 70)"
        print(f"RSI信号: {rsi_signal}")
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
