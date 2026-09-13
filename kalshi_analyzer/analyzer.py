"""Core P&L analyzer for Kalshi trading data."""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Optional, Tuple
from pathlib import Path

from .models import TradeData, PerformanceMetrics


class KalshiAnalyzer:
    """Analyzes Kalshi CSV exports for trading performance."""

    def __init__(self, csv_path: Optional[str] = None):
        """Initialize analyzer with optional CSV file.
        
        Args:
            csv_path: Path to Kalshi CSV export file
        """
        self.df = None
        self.trades: List[TradeData] = []
        self.metrics = None

        if csv_path:
            self.load_csv(csv_path)

    def load_csv(self, csv_path: str) -> None:
        """Load and clean Kalshi CSV data.
        
        Args:
            csv_path: Path to CSV file
        """
        self.df = pd.read_csv(csv_path)
        self._clean_data()
        self._parse_trades()

    def _clean_data(self) -> None:
        """Clean and normalize DataFrame columns."""
        # Parse timestamps
        self.df["open_timestamp"] = pd.to_datetime(self.df["open_timestamp"])
        self.df["close_timestamp"] = pd.to_datetime(self.df["close_timestamp"])

        # Numeric columns
        numeric_cols = [
            "quantity_fp",
            "entry_price_dollars",
            "exit_price_dollars",
            "open_fees_dollars",
            "close_fees_dollars",
            "realized_pnl_without_fees_dollars",
            "realized_pnl_with_fees_dollars",
        ]

        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        # Extract ticker from market_ticker
        self.df["ticker"] = self.df["market_ticker"].str.extract(r"^(KX[A-Z]+15M)")[0]

    def _parse_trades(self) -> None:
        """Convert DataFrame rows to TradeData objects."""
        self.trades = []
        for _, row in self.df.iterrows():
            trade = TradeData(
                ticker=row["ticker"] or "UNKNOWN",
                quantity=float(row["quantity_fp"] or 0),
                entry_price=float(row["entry_price_dollars"] or 0),
                exit_price=float(row["exit_price_dollars"] or 0),
                open_fees=float(row["open_fees_dollars"] or 0),
                close_fees=float(row["close_fees_dollars"] or 0),
                realized_pnl_without_fees=float(
                    row["realized_pnl_without_fees_dollars"] or 0
                ),
                realized_pnl_with_fees=float(row["realized_pnl_with_fees_dollars"] or 0),
                open_timestamp=row["open_timestamp"],
                close_timestamp=row["close_timestamp"],
                market_ticker=row["market_ticker"],
            )
            self.trades.append(trade)

    def calculate_metrics(self) -> PerformanceMetrics:
        """Calculate comprehensive performance metrics.
        
        Returns:
            PerformanceMetrics object with aggregated stats
        """
        if not self.trades:
            return PerformanceMetrics(
                total_pnl_with_fees=0,
                total_pnl_without_fees=0,
                total_fees=0,
                win_count=0,
                loss_count=0,
                total_trades=0,
                win_rate=0.0,
            )

        total_pnl_with_fees = sum(t.realized_pnl_with_fees for t in self.trades)
        total_pnl_without_fees = sum(t.realized_pnl_without_fees for t in self.trades)
        total_fees = sum(t.total_fees for t in self.trades)

        wins = [t for t in self.trades if t.is_win]
        losses = [t for t in self.trades if not t.is_win]

        win_count = len(wins)
        loss_count = len(losses)
        total_trades = len(self.trades)
        win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0

        avg_win = (
            np.mean([t.realized_pnl_with_fees for t in wins]) if wins else None
        )
        avg_loss = (
            np.mean([t.realized_pnl_with_fees for t in losses]) if losses else None
        )

        largest_win = max([t.realized_pnl_with_fees for t in wins]) if wins else None
        largest_loss = min([t.realized_pnl_with_fees for t in losses]) if losses else None

        # Calculate profit factor
        gross_profit = sum(t.realized_pnl_with_fees for t in wins) if wins else 0
        gross_loss = abs(sum(t.realized_pnl_with_fees for t in losses)) if losses else 0
        profit_factor = (
            gross_profit / gross_loss if gross_loss > 0 else None
        )

        # Average hold time
        avg_hold_time = (
            np.mean([t.hold_time_minutes for t in self.trades])
            if self.trades
            else None
        )

        self.metrics = PerformanceMetrics(
            total_pnl_with_fees=total_pnl_with_fees,
            total_pnl_without_fees=total_pnl_without_fees,
            total_fees=total_fees,
            win_count=win_count,
            loss_count=loss_count,
            total_trades=total_trades,
            win_rate=win_rate,
            avg_win=avg_win,
            avg_loss=avg_loss,
            profit_factor=profit_factor,
            largest_win=largest_win,
            largest_loss=largest_loss,
            avg_hold_time_minutes=avg_hold_time,
        )

        return self.metrics

    def get_trades_by_ticker(self, ticker: str) -> List[TradeData]:
        """Get all trades for a specific ticker.
        
        Args:
            ticker: Ticker symbol
            
        Returns:
            List of trades for that ticker
        """
        return [t for t in self.trades if t.ticker == ticker]

    def get_top_performers(self, n: int = 5) -> List[Tuple[str, float]]:
        """Get top N performing tickers.
        
        Args:
            n: Number of top performers to return
            
        Returns:
            List of (ticker, pnl) tuples
        """
        ticker_pnl = {}
        for trade in self.trades:
            if trade.ticker not in ticker_pnl:
                ticker_pnl[trade.ticker] = 0
            ticker_pnl[trade.ticker] += trade.realized_pnl_with_fees

        sorted_tickers = sorted(ticker_pnl.items(), key=lambda x: x[1], reverse=True)
        return sorted_tickers[:n]

    def get_bottom_performers(self, n: int = 5) -> List[Tuple[str, float]]:
        """Get bottom N performing tickers.
        
        Args:
            n: Number of bottom performers to return
            
        Returns:
            List of (ticker, pnl) tuples
        """
        ticker_pnl = {}
        for trade in self.trades:
            if trade.ticker not in ticker_pnl:
                ticker_pnl[trade.ticker] = 0
            ticker_pnl[trade.ticker] += trade.realized_pnl_with_fees

        sorted_tickers = sorted(ticker_pnl.items(), key=lambda x: x[1])
        return sorted_tickers[:n]

    def filter_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[TradeData]:
        """Filter trades by date range.
        
        Args:
            start_date: Start datetime
            end_date: End datetime
            
        Returns:
            List of trades within date range
        """
        return [
            t
            for t in self.trades
            if start_date <= t.close_timestamp <= end_date
        ]
