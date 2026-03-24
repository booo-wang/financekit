"""
FinanceKit: A professional financial data crawler and analysis framework
金融数据爬虫和分析框架

Features:
- 多源金融数据爬虫 (股票、加密货币)
- 技术指标计算 (SMA, EMA, MACD, RSI, 布林线)
- 统计分析 (收益率、波动率、夏普比率、最大回撤)
- 特征提取 (价格、波动率、动量)
- 高效缓存机制
- 完整的日志系统
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="financekit",
    version="0.2.0",
    author="booo-wang",
    author_email="christinjack_@outlook.com",
    description="A professional financial data crawler and analysis framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/booo-wang/financekit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "requests>=2.26.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.7b0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "financekit=financekit.cli:main",
        ],
    },
)
