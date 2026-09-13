# Kalshi P&L Analyzer Bot

A powerful Python bot for analyzing Kalshi trading performance from CSV exports. Get instant insights into your trading metrics, win rates, and performance across different tickers.

## Features

✅ **Comprehensive Analysis**
- Total P&L (with and without fees)
- Win/loss rates and counts
- Average win/loss calculations
- Profit factor metrics
- Hold time analysis

✅ **Ticker Performance**
- Top performing tickers
- Bottom performing tickers
- Per-ticker P&L tracking

✅ **Date Range Filtering**
- Filter trades by date range
- Time-based performance analysis

✅ **Export Capabilities**
- JSON export for further analysis
- Formatted console reports
- Tabular output

## Installation

```bash
git clone https://github.com/jlindsey031088-sudo/kalshi-pnl-analyzer-bot.git
cd kalshi-pnl-analyzer-bot

pip install -r requirements.txt
```

## Quick Start

### Analyze a CSV file:

```bash
python main.py analyze your_kalshi_export.csv
```

### With custom options:

```bash
# Show top 10 and bottom 10 performers
python main.py analyze your_kalshi_export.csv --top 10 --bottom 10

# Export results to JSON
python main.py analyze your_kalshi_export.csv --export results.json
```

## Usage in Python

```python
from kalshi_analyzer import KalshiAnalyzer
from kalshi_analyzer.reporter import ReportGenerator

# Load and analyze
analyzer = KalshiAnalyzer('your_kalshi_export.csv')
metrics = analyzer.calculate_metrics()

# Print reports
ReportGenerator.print_summary(metrics)
ReportGenerator.print_top_performers(analyzer, n=5)

# Access individual trades
trades = analyzer.get_trades_by_ticker('KXABC15M')
for trade in trades:
    print(f"Trade: {trade.ticker}, P&L: ${trade.realized_pnl_with_fees}")
```

## CSV Format

Expect your Kalshi CSV export to have these columns:
- `market_ticker`
- `open_timestamp`
- `close_timestamp`
- `quantity_fp`
- `entry_price_dollars`
- `exit_price_dollars`
- `open_fees_dollars`
- `close_fees_dollars`
- `realized_pnl_without_fees_dollars`
- `realized_pnl_with_fees_dollars`

## API Reference

### KalshiAnalyzer

#### Methods

- `load_csv(csv_path)` - Load CSV file
- `calculate_metrics()` - Get PerformanceMetrics
- `get_trades_by_ticker(ticker)` - Get trades for a ticker
- `get_top_performers(n)` - Get top N tickers by P&L
- `get_bottom_performers(n)` - Get bottom N tickers by P&L
- `filter_by_date_range(start, end)` - Filter by dates

### PerformanceMetrics

#### Properties

- `total_pnl_with_fees` - Net P&L after fees
- `total_pnl_without_fees` - Gross P&L
- `total_fees` - Sum of all fees
- `win_count` - Number of winning trades
- `loss_count` - Number of losing trades
- `win_rate` - Win rate percentage
- `avg_win` - Average winning trade
- `avg_loss` - Average losing trade
- `profit_factor` - Gross profit / Gross loss
- `largest_win` - Best trade
- `largest_loss` - Worst trade
- `avg_hold_time_minutes` - Average holding time

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=kalshi_analyzer
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or suggestions, please open a GitHub issue.

---

**Built by winning traders, for winning traders.** 🚀
