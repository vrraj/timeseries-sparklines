# timeseries-svg

A general-purpose Python library for rendering time series data as SVG charts and sparklines. Accepts JSONB data from any source (realtime for sparklines or historical data) and produces clean, interactive SVG visualizations.

## Features

- **Flexible data input**: Accepts multiple JSONB formats (list of dicts, list of lists, dict with date keys, or simple value lists)
- **Sparkline rendering**: Compact sparkline charts for inline display
- **Interactive charts**: Full time series charts with hover interactions, tooltips, and axis labels
- **Configurable styling**: Customizable colors, dimensions, and formatting
- **Zero external dependencies**: Pure Python, no heavy plotting libraries required
- **SVG output**: Lightweight, scalable vector graphics perfect for web embedding

## Installation

```bash
pip install timeseries-svg
```

Or install from source:

```bash
git clone https://github.com/yourusername/timeseries-svg.git
cd timeseries-svg
pip install -e .
```

## Quick Start

### Sparkline Example

```python
from timeseries_svg import SparklineRenderer

# Input data can be in various formats
data = [
    {"d": "2024-01-01", "c": 100.0},
    {"d": "2024-01-02", "c": 102.5},
    {"d": "2024-01-03", "c": 101.2},
    {"d": "2024-01-04", "c": 105.0},
]

renderer = SparklineRenderer(width=96, height=24)
svg = renderer.render(data)
print(svg)  # Returns SVG string
```

### Time Series Chart Example

```python
from timeseries_svg import TimeSeriesChartRenderer

# Historical price data
data = [
    {"d": "2024-01-01", "c": 150.0},
    {"d": "2024-01-02", "c": 152.5},
    {"d": "2024-01-03", "c": 151.0},
    {"d": "2024-01-04", "c": 155.0},
    {"d": "2024-01-05", "c": 158.0},
]

renderer = TimeSeriesChartRenderer(width=760, height=320)
svg = renderer.render(data, period="5D", title="AAPL Price History")
print(svg)  # Returns interactive SVG string
```

## Data Input Formats

The library automatically normalizes various input formats. Use the format that best matches your data source:

### List of Dicts (Standard Format)
Recommended for most use cases. Uses `d` for date and `c` for close/value.

```python
data = [
    {"d": "2024-01-01", "c": 100.0},
    {"d": "2024-01-02", "c": 102.5},
    {"d": "2024-01-03", "c": 101.2},
    {"d": "2024-01-04", "c": 105.0},
]
```

### List of Lists
Each inner list is `[date, value]`:

```python
data = [
    ["2024-01-01", 100.0],
    ["2024-01-02", 102.5],
    ["2024-01-03", 101.2],
]
```

### Dict with Date Keys
Date strings as keys, values as the data:

```python
data = {
    "2024-01-01": 100.0,
    "2024-01-02": 102.5,
    "2024-01-03": 101.2,
}
```

### Simple Value List
Auto-generates dates as "day-0", "day-1", etc. Best for sparklines where dates don't matter:

```python
data = [100.0, 102.5, 101.2, 105.0]
```

### Custom Keys
If your data uses different key names, specify them:

```python
data = [
    {"date": "2024-01-01", "price": 100.0},
    {"date": "2024-01-02", "price": 102.5},
]

renderer.render(data, date_key="date", value_key="price")
```

### Nested Format (JSONB from databases)
Common format for database JSONB storage:

```python
data = {
    "history": [
        {"d": "2024-01-01", "c": 100.0},
        {"d": "2024-01-02", "c": 102.5},
    ]
}

# The library extracts the array automatically
```

## Configuration

### Sparkline Renderer

```python
renderer = SparklineRenderer(
    width=96,              # SVG width in pixels
    height=24,             # SVG height in pixels
    stroke_width=1.8,      # Line stroke width
    baseline_color="rgba(148,163,184,0.35)",  # Baseline color
    up_color="#12b76a",    # Upward trend color
    down_color="#f04438",  # Downward trend color
    show_baseline=True,    # Show baseline reference line
)
```

### Chart Renderer

```python
renderer = TimeSeriesChartRenderer(
    width=760,              # SVG width in pixels
    height=320,             # SVG height in pixels
    margin={'top': 16, 'right': 20, 'bottom': 44, 'left': 58},  # Chart margins
    up_color="#16a34a",     # Upward trend color
    down_color="#dc2626",   # Downward trend color
    grid_color="rgba(148,163,184,0.35)",  # Grid line color
    axis_color="#94a3b8",   # Axis line color
    label_color="#64748b",  # Axis label color
)
```

## Period Formatting

Charts support different time periods for label formatting:

- `5D`: Daily labels (weekday)
- `1M`: Weekly labels (month day)
- `3M`: Every 3 weeks (month day)
- `6M`: Monthly labels (month)
- `1Y`: Every 2 months (month)

```python
renderer.render(data, period="1M")  # Use 1M label formatting
```

## Data Normalization

Use the data normalization utilities directly if needed:

```python
from timeseries_svg import normalize_timeseries_data, extract_values, extract_dates

normalized = normalize_timeseries_data(data)
values = extract_values(normalized)
dates = extract_dates(normalized)
```

## Use Cases

- **Financial dashboards**: Stock price sparklines and historical charts
- **IoT monitoring**: Real-time sensor data visualization
- **Analytics platforms**: Time series metrics and trends
- **Trading applications**: Price history and technical indicators
- **Any web application**: Lightweight SVG charts without heavy dependencies

## Integration with Web Frameworks

### FastAPI Example

```python
from fastapi import FastAPI
from timeseries_svg import SparklineRenderer

app = FastAPI()
renderer = SparklineRenderer()

@app.get("/sparkline/{symbol}")
async def get_sparkline(symbol: str):
    # Fetch data from your database/API
    data = await fetch_price_data(symbol)
    svg = renderer.render(data)
    return Response(content=svg, media_type="image/svg+xml")
```

### Flask Example

```python
from flask import Flask, Response
from timeseries_svg import TimeSeriesChartRenderer

app = Flask(__name__)
renderer = TimeSeriesChartRenderer()

@app.route("/chart/<symbol>")
def chart(symbol):
    data = fetch_historical_data(symbol)
    svg = renderer.render(data, period="1M")
    return Response(svg, mimetype="image/svg+xml")
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
