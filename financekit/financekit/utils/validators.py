"""数据验证模块"""

import re
from datetime import datetime
from typing import Tuple


def validate_symbol(symbol: str) -> bool:
    """
    验证股票/加密货币符号

    Args:
        symbol: 股票或加密货币符号

    Returns:
        是否有效
    """
    # 支持 AAPL, BTC-USD, AAPL.HK 等格式
    return bool(re.match(r"^[A-Za-z0-9]{1,10}(-[A-Za-z]{1,5})?(\.[A-Za-z]{1,4})?$", symbol))


def validate_date_range(start_date: datetime, end_date: datetime) -> Tuple[bool, str]:
    """
    验证日期范围

    Args:
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
        return False, "日期必须是datetime对象"

    if start_date > end_date:
        return False, "开始日期不能晚于结束日期"

    if (end_date - start_date).days > 10 * 365:
        return False, "时间跨度不能超过10年"

    return True, ""


def validate_price(price: float) -> bool:
    """验证价格"""
    return isinstance(price, (int, float)) and price > 0


def validate_volume(volume: int) -> bool:
    """验证成交量"""
    return isinstance(volume, int) and volume >= 0
