---
layout: default
title: "API Reference | Timeseries SVG"
description: "Complete API documentation for SparklineRenderer, TimeSeriesChartRenderer, and data utilities."
---

# API Reference

This document provides the complete API reference for the timeseries-sparklines library, including class constructors, method signatures, parameter details, and common usage patterns.

> **New here?** Start with the project overview on the home page: **[timeseries-sparklines docs home](https://vrraj.github.io/timeseries-sparklines/)**.
>
> **Source + releases:** GitHub repo and PyPI package are linked from the home page.

## Table of Contents

- [Core Classes](#core-classes)
- [Sparkline Renderer API](#sparkline-renderer-api)
- [Chart Renderer API](#chart-renderer-api)
- [Data Normalization API](#data-normalization-api)
- [Common Usage Patterns](#common-usage-patterns)

---

## Core Classes

### `SparklineRenderer`

Render compact sparkline SVG charts from time series data.

```python
class SparklineRenderer:
    def __init__(
        self,
        width: int = 96,
        height: int = 32,
        stroke_width: float = 1.8,
        baseline_color: str = "rgba(148,163,184,0.35)",
        up_color: str = "#12b76a",
        down_color: str = "#f04438",
        show_baseline: bool = True,
        color_by_open: bool = False,
    )
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `width` | `int` | 96 | SVG width in pixels |
| `height` | `int` | 32 | SVG height in pixels |
| `stroke_width` | `float` | 1.8 | Line stroke width |
| `baseline_color` | `str` | "rgba(148,163,184,0.35)" | Color for baseline reference line |
| `up_color` | `str` | "#12b76a" | Color for upward trend |
| `down_color` | `str` | "#f04438" | Color for downward trend |
| `show_baseline` | `bool` | True | Whether to show baseline reference line |
| `color_by_open` | `bool` | False | If True, color segments based on open price (first point) |

### `TimeSeriesChartRenderer`

Render interactive time series chart SVGs with axis labels and grid lines.

```python
class TimeSeriesChartRenderer:
    def __init__(
        self,
        width: int = 760,
        height: int = 320,
        margin: Optional[Dict[str, int]] = None,
        up_color: str = "#16a34a",
        down_color: str = "#dc2626",
        grid_color: str = "rgba(148,163,184,0.35)",
        axis_color: str = "#94a3b8",
        label_color: str = "#64748b",
        tooltip_bg: str = "#ffffff",
        tooltip_border: str = "rgba(148,163,184,0.45)",
        color_by_open: bool = False,
        y_axis_label: Optional[str] = None,
        y_axis_offset: float = 0.1,
    )
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `width` | `int` | 760 | SVG width in pixels |
| `height` | `int` | 320 | SVG height in pixels |
| `margin` | `Dict[str, int]` | {top: 16, right: 20, bottom: 44, left: 58} | Chart margins |
| `up_color` | `str` | "#16a34a" | Color for upward trend |
| `down_color` | `str` | "#dc2626" | Color for downward trend |
| `grid_color` | `str` | "rgba(148,163,184,0.35)" | Grid line color |
| `axis_color` | `str` | "#94a3b8" | Axis line color |
| `label_color` | `str` | "#64748b" | Axis label color |
| `tooltip_bg` | `str` | "#ffffff" | Tooltip background color |
| `tooltip_border` | `str` | "rgba(148,163,184,0.45)" | Tooltip border color |
| `color_by_open` | `bool` | False | If True, color segments based on open price (first point) |
| `y_axis_label` | `str` | None | Optional label for y-axis (e.g., '°C', '°F', '$') |
| `y_axis_offset` | `float` | 0.1 | Y-axis offset as fraction of range (default 0.1 = 10%) |

### `BarChartRenderer`

Render time series bar chart SVGs with axis labels and grid lines.

```python
class BarChartRenderer:
    def __init__(
        self,
        width: int = 760,
        height: int = 320,
        margin: Optional[Dict[str, int]] = None,
        bar_color: str = "#3b82f6",
        bar_width_ratio: float = 0.7,
        grid_color: str = "rgba(148,163,184,0.35)",
        axis_color: str = "#94a3b8",
        label_color: str = "#64748b",
        color_by_open: bool = False,
        up_color: str = "#16a34a",
        down_color: str = "#dc2626",
        y_axis_label: Optional[str] = None,
        y_axis_offset: float = 0.1,
    )
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `width` | `int` | 760 | SVG width in pixels |
| `height` | `int` | 320 | SVG height in pixels |
| `margin` | `Dict[str, int]` | {top: 16, right: 20, bottom: 44, left: 58} | Chart margins |
| `bar_color` | `str` | "#3b82f6" | Default bar color |
| `bar_width_ratio` | `float` | 0.7 | Ratio of bar width to available space (0-1) |
| `grid_color` | `str` | "rgba(148,163,184,0.35)" | Grid line color |
| `axis_color` | `str` | "#94a3b8" | Axis line color |
| `label_color` | `str` | "#64748b" | Axis label color |
| `color_by_open` | `bool` | False | If True, color bars based on open price (first point) |
| `up_color` | `str` | "#16a34a" | Color for bars above open price |
| `down_color` | `str` | "#dc2626" | Color for bars below open price |
| `y_axis_label` | `str` | None | Optional label for y-axis (e.g., '°C', '°F', '$') |
| `y_axis_offset` | `float` | 0.1 | Y-axis offset as fraction of range (default 0.1 = 10%) |

**render() method:** Same signature as TimeSeriesChartRenderer

---

## Sparkline Renderer API

### `render()`

Render sparkline SVG from input data.

```python
def render(self, data: Any, **normalize_kwargs) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `data` | `Any` | ✅ | Input data in any supported format (list, dict, etc.) |
| `date_key` | `str` | ❌ | Key name for date in dict format (default: "d") |
| `value_key` | `str` | ❌ | Key name for value in dict format (default: "c") |
| `date_format` | `str` | ❌ | Optional strftime format for date parsing |

**Returns:** `str` - SVG string

**Example:**

```python
from timeseries_svg import SparklineRenderer

renderer = SparklineRenderer(width=96, height=32)

# Basic usage
data = [
    {"d": "2024-01-01", "v": 100.0},
    {"d": "2024-01-02", "v": 102.5},
    {"d": "2024-01-03", "v": 101.2},
]
svg = renderer.render(data)

# With custom keys
data = [
    {"date": "2024-01-01", "price": 100.0},
    {"date": "2024-01-02", "price": 102.5},
]
svg = renderer.render(data, date_key="date", value_key="price")

# With color by open
svg = renderer.render(data, color_by_open=True)
```

---

## Chart Renderer API

### `render()`

Render time series chart SVG with axis labels and grid lines.

```python
def render(
    self,
    data: Any,
    period: str = "1M",
    title: Optional[str] = None,
    **normalize_kwargs
) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `data` | `Any` | ✅ | Input data in any supported format |
| `period` | `str` | ❌ | Time period for label formatting (5D, 1M, 3M, 6M, 1Y) |
| `title` | `str` | ❌ | Optional chart title |
| `date_key` | `str` | ❌ | Key name for date in dict format (default: "d") |
| `value_key` | `str` | ❌ | Key name for value in dict format (default: "c") |
| `date_format` | `str` | ❌ | Optional strftime format for date parsing |

**Period Options:**

| Period | Description | Time Window |
|--------|-------------|-------------|
| `5D` | Daily labels (weekday) | 5 calendar days |
| `1W` | Weekly labels | 7 calendar days |
| `2W` | Bi-weekly labels | 14 calendar days |
| `1M` | Weekly labels (month day) | 30 calendar days |
| `3M` | Every 3 weeks (month day) | 90 calendar days |
| `6M` | Monthly labels (month) | 180 calendar days |
| `1Y` | Every 2 months (month) | 365 calendar days |

**Custom Periods:**

You can also pass a custom `timedelta` object for any time window:

```python
from datetime import timedelta

# Custom 2-week period
svg = renderer.render(data, period=timedelta(weeks=2))

# Custom 45-day period
svg = renderer.render(data, period=timedelta(days=45))

# Custom 3-hour period (for intraday data)
svg = renderer.render(data, period=timedelta(hours=3))
```

**Returns:** `str` - SVG string

**Example:**

```python
from timeseries_svg import TimeSeriesChartRenderer

renderer = TimeSeriesChartRenderer(width=760, height=320)

# Basic usage
data = [
    {"d": "2024-01-01", "v": 150.0},
    {"d": "2024-01-02", "v": 152.5},
    {"d": "2024-01-03", "v": 151.0},
]
svg = renderer.render(data, period="1M", title="AAPL Price History")

# With color by open
svg = renderer.render(data, period="5D", color_by_open=True)
```

---

## Data Normalization API

### `normalize_timeseries_data()`

Normalize various JSONB input formats into a standard time series structure.

```python
def normalize_timeseries_data(
    data: Any,
    date_key: str = "d",
    value_key: str = "v",
    date_format: Optional[str] = None
) -> List[Dict[str, Any]]
```

**Supported Input Formats:**

1. **List of dicts:** `[{"d": "2024-01-01", "v": 100.0}, ...]`
2. **List of lists:** `[["2024-01-01", 100.0], ...]`
3. **Dict with date keys:** `{"2024-01-01": 100.0, ...}`
4. **List of values:** `[100.0, 101.0, ...]` (dates auto-generated)

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | `Any` | - | Input data in various formats |
| `date_key` | `str` | "d" | Key name for date in dict format |
| `value_key` | `str` | "c" | Key name for value in dict format |
| `date_format` | `str` | None | Optional strftime format for date parsing |

**Returns:** `List[Dict[str, Any]]` - List of dicts with standardized "date" and "value" keys

**Example:**

```python
from timeseries_svg import normalize_timeseries_data

# List of dicts
data = [{"d": "2024-01-01", "v": 100.0}]
normalized = normalize_timeseries_data(data)
# Returns: [{"date": "2024-01-01", "value": 100.0}]

# List of lists
data = [["2024-01-01", 100.0]]
normalized = normalize_timeseries_data(data)
# Returns: [{"date": "2024-01-01", "value": 100.0}]

# Dict with date keys
data = {"2024-01-01": 100.0}
normalized = normalize_timeseries_data(data)
# Returns: [{"date": "2024-01-01", "value": 100.0}]

# List of values
data = [100.0, 101.0, 102.0]
normalized = normalize_timeseries_data(data)
# Returns: [{"date": "day-0", "value": 100.0}, {"date": "day-1", "value": 101.0}, ...]
```

### `extract_values()`

Extract just the values from normalized data.

```python
def extract_values(normalized_data: List[Dict[str, Any]]) -> List[float]
```

**Example:**

```python
from timeseries_svg import normalize_timeseries_data, extract_values

data = [{"d": "2024-01-01", "v": 100.0}, {"d": "2024-01-02", "v": 102.5}]
normalized = normalize_timeseries_data(data)
values = extract_values(normalized)
# Returns: [100.0, 102.5]
```

### `extract_dates()`

Extract just the dates from normalized data.

```python
def extract_dates(normalized_data: List[Dict[str, Any]]) -> List[str]
```

**Example:**

```python
from timeseries_svg import normalize_timeseries_data, extract_dates

data = [{"d": "2024-01-01", "v": 100.0}, {"d": "2024-01-02", "v": 102.5}]
normalized = normalize_timeseries_data(data)
dates = extract_dates(normalized)
# Returns: ["2024-01-01", "2024-01-02"]
```

---

## Common Usage Patterns

### 1. Basic Sparkline Rendering

```python
from timeseries_svg import SparklineRenderer

renderer = SparklineRenderer(width=96, height=32)
data = [
    {"d": "2024-01-01", "v": 100.0},
    {"d": "2024-01-02", "v": 102.5},
    {"d": "2024-01-03", "v": 101.2},
]
svg = renderer.render(data)
```

### 2. Chart with Period Slicing

```python
from timeseries_svg import TimeSeriesChartRenderer

renderer = TimeSeriesChartRenderer(width=760, height=320)
data = get_historical_data()  # Your data source

# Show last 5 days
svg = renderer.render(data, period="5D", title="5 Day Chart")

# Show last month
svg = renderer.render(data, period="1M", title="1 Month Chart")

# Show last year
svg = renderer.render(data, period="1Y", title="1 Year Chart")
```

### 3. Color by Open Price

```python
from timeseries_svg import SparklineRenderer

renderer = SparklineRenderer(color_by_open=True)
svg = renderer.render(data)
# Segments above open price are green, below are red
```

### 4. Custom Data Keys

```python
from timeseries_svg import SparklineRenderer

renderer = SparklineRenderer()
data = [
    {"date": "2024-01-01", "price": 100.0},
    {"date": "2024-01-02", "price": 102.5},
]
svg = renderer.render(data, date_key="date", value_key="price")
```

### 5. Simple Value List

```python
from timeseries_svg import SparklineRenderer

renderer = SparklineRenderer()
data = [100.0, 102.5, 101.2, 105.0, 103.8]
svg = renderer.render(data)
# Dates auto-generated as "day-0", "day-1", etc.
```

### 6. Custom Styling

```python
from timeseries_svg import SparklineRenderer

renderer = SparklineRenderer(
    width=120,
    height=40,
    stroke_width=2.0,
    up_color="#00ff00",
    down_color="#ff0000",
    baseline_color="#cccccc",
    show_baseline=True,
)
svg = renderer.render(data)
```

### 7. Integration with FastAPI

```python
from fastapi import FastAPI, Response
from timeseries_svg import SparklineRenderer

app = FastAPI()
renderer = SparklineRenderer()

@app.post("/sparkline")
async def get_sparkline(request: dict):
    data = request.get("data")
    svg = renderer.render(data, color_by_open=True)
    return Response(content=svg, media_type="image/svg+xml")
```

### 8. Integration with Flask

```python
from flask import Flask, Response
from timeseries_svg import TimeSeriesChartRenderer

app = Flask(__name__)
renderer = TimeSeriesChartRenderer()

@app.route("/chart/<symbol>")
def chart(symbol):
    data = fetch_historical_data(symbol)
    svg = renderer.render(data, period="1M", title=f"{symbol} Price History")
    return Response(svg, mimetype="image/svg+xml")
```

---

## Parameter Stability

### Stable Parameters

| Parameter | Stability | Notes |
|-----------|-----------|-------|
| `width` | ✅ Stable | SVG width in pixels |
| `height` | ✅ Stable | SVG height in pixels |
| `stroke_width` | ✅ Stable | Line stroke width |
| `up_color` | ✅ Stable | Color for upward trend |
| `down_color` | ✅ Stable | Color for downward trend |
| `period` | ✅ Stable | Time period for chart labels (5D, 1M, 3M, 6M, 1Y) |
| `date_key` | ✅ Stable | Key name for date in dict format |
| `value_key` | ✅ Stable | Key name for value in dict format |
| `color_by_open` | ✅ Stable | If True, color segments based on open price |

**Legend:**
- ✅ **Stable**: Guaranteed interface, won't change
