"""Data models for Kalshi trading data."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TradeData:
    """Represents a single trade from Kalshi."""

    ticker: str
    quantity: float
    entry_price: float
    exit_price: float
    open_fees: float
    close_fees: float
    realized_pnl_without_fees: float
    realized_pnl_with_fees: float
    open_timestamp: datetime
    close_timestamp: datetime
    market_ticker: str

    @property
    def is_win(self) -> bool:
        """Check if trade was profitable."""
        return self.realized_pnl_with_fees > 0

    @property
    def total_fees(self) -> float:
        """Calculate total fees for trade."""
        return self.open_fees + self.close_fees

    @property
    def hold_time_minutes(self) -> float:
        """Calculate how long position was held in minutes."""
        if self.close_timestamp and self.open_timestamp:
            delta = self.close_timestamp - self.open_timestamp
            return delta.total_seconds() / 60
        return 0


@dataclass
class PerformanceMetrics:
    """Aggregated performance metrics."""

    total_pnl_with_fees: float
    total_pnl_without_fees: float
    total_fees: float
    win_count: int
    loss_count: int
    total_trades: int
    win_rate: float
    avg_win: Optional[float] = None
    avg_loss: Optional[float] = None
    profit_factor: Optional[float] = None
    largest_win: Optional[float] = None
    largest_loss: Optional[float] = None
    avg_hold_time_minutes: Optional[float] = None

    @property
    def loss_rate(self) -> float:
        """Calculate loss rate percentage."""
        if self.total_trades == 0:
            return 0.0
        return (self.loss_count / self.total_trades) * 100

    @property
    def roi(self) -> float:
        """Calculate ROI based on initial capital (estimated from position size)."""
        if self.total_pnl_with_fees == 0:
            return 0.0
        return self.total_pnl_with_fees
