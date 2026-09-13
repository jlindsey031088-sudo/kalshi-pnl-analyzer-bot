"""Report generation for trading analysis."""

from typing import Optional
from tabulate import tabulate
from .models import PerformanceMetrics
from .analyzer import KalshiAnalyzer


class ReportGenerator:
    """Generates human-readable reports from analysis."""

    @staticmethod
    def print_summary(metrics: PerformanceMetrics) -> None:
        """Print summary performance report.
        
        Args:
            metrics: PerformanceMetrics object
        """
        print("\n" + "="*60)
        print("KALSHI P&L ANALYSIS SUMMARY")
        print("="*60)

        summary_data = [
            ["Total P&L (with fees)", f"${metrics.total_pnl_with_fees:.2f}"],
            ["Gross P&L (without fees)", f"${metrics.total_pnl_without_fees:.2f}"],
            ["Total Fees", f"${metrics.total_fees:.2f}"],
            ["Total Trades", metrics.total_trades],
            ["Wins", metrics.win_count],
            ["Losses", metrics.loss_count],
            ["Win Rate", f"{metrics.win_rate:.2f}%"],
            ["Loss Rate", f"{metrics.loss_rate:.2f}%"],
        ]

        if metrics.avg_win is not None:
            summary_data.append(["Average Win", f"${metrics.avg_win:.2f}"])
        if metrics.avg_loss is not None:
            summary_data.append(["Average Loss", f"${metrics.avg_loss:.2f}"])
        if metrics.profit_factor is not None:
            summary_data.append(["Profit Factor", f"{metrics.profit_factor:.2f}"])
        if metrics.largest_win is not None:
            summary_data.append(["Largest Win", f"${metrics.largest_win:.2f}"])
        if metrics.largest_loss is not None:
            summary_data.append(["Largest Loss", f"${metrics.largest_loss:.2f}"])
        if metrics.avg_hold_time_minutes is not None:
            summary_data.append(
                ["Avg Hold Time", f"{metrics.avg_hold_time_minutes:.1f} min"]
            )

        print(tabulate(summary_data, tablefmt="grid"))
        print()

    @staticmethod
    def print_top_performers(analyzer: KalshiAnalyzer, n: int = 5) -> None:
        """Print top performing tickers.
        
        Args:
            analyzer: KalshiAnalyzer instance
            n: Number of top performers to show
        """
        top_performers = analyzer.get_top_performers(n)
        print("\n" + "="*60)
        print(f"TOP {n} PERFORMING TICKERS")
        print("="*60)

        data = [[ticker, f"${pnl:.2f}"] for ticker, pnl in top_performers]
        print(tabulate(data, headers=["Ticker", "P&L"], tablefmt="grid"))
        print()

    @staticmethod
    def print_bottom_performers(analyzer: KalshiAnalyzer, n: int = 5) -> None:
        """Print bottom performing tickers.
        
        Args:
            analyzer: KalshiAnalyzer instance
            n: Number of bottom performers to show
        """
        bottom_performers = analyzer.get_bottom_performers(n)
        print("\n" + "="*60)
        print(f"BOTTOM {n} PERFORMING TICKERS")
        print("="*60)

        data = [[ticker, f"${pnl:.2f}"] for ticker, pnl in bottom_performers]
        print(tabulate(data, headers=["Ticker", "P&L"], tablefmt="grid"))
        print()

    @staticmethod
    def export_summary_json(metrics: PerformanceMetrics, filepath: str) -> None:
        """Export metrics to JSON.
        
        Args:
            metrics: PerformanceMetrics object
            filepath: Path to save JSON file
        """
        import json

        data = {
            "total_pnl_with_fees": metrics.total_pnl_with_fees,
            "total_pnl_without_fees": metrics.total_pnl_without_fees,
            "total_fees": metrics.total_fees,
            "win_count": metrics.win_count,
            "loss_count": metrics.loss_count,
            "total_trades": metrics.total_trades,
            "win_rate": metrics.win_rate,
            "loss_rate": metrics.loss_rate,
            "avg_win": metrics.avg_win,
            "avg_loss": metrics.avg_loss,
            "profit_factor": metrics.profit_factor,
            "largest_win": metrics.largest_win,
            "largest_loss": metrics.largest_loss,
            "avg_hold_time_minutes": metrics.avg_hold_time_minutes,
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Summary exported to {filepath}")
