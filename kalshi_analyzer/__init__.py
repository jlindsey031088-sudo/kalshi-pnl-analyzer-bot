"""Kalshi P&L Analyzer Bot - Analyze and track trading performance."""

__version__ = "1.0.0"
__author__ = "Trading Bot"

from .analyzer import KalshiAnalyzer
from .models import TradeData, PerformanceMetrics

__all__ = ["KalshiAnalyzer", "TradeData", "PerformanceMetrics"]
