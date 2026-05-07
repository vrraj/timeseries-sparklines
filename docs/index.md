---
layout: default
title: "Timeseries SVG: Time Series Visualization"
description: "A lightweight Python library for rendering time series data as SVG charts and sparklines. Accepts JSONB data from any source and produces clean, interactive SVG visualizations."
---

# timeseries-sparklines

<p align="left">
  <a href="https://pypi.org/project/timeseries-sparklines/">
    <img src="https://img.shields.io/pypi/v/timeseries-sparklines?color=blue&logo=pypi&logoColor=white" alt="PyPI - Version">
  </a>
  <a href="https://github.com/vrraj/timeseries-sparklines/releases">
    <img src="https://img.shields.io/github/v/release/vrraj/timeseries-sparklines?label=github%20release&color=orange&logo=github" alt="GitHub Release">
  </a>
</p>

A lightweight **Python library for rendering time series data as SVG charts and sparklines**. Accepts JSONB data from any source (realtime for sparklines or historical data) and produces clean, interactive SVG visualizations.

```
pip install timeseries-sparklines
```

Includes an **Interactive Test UI** for testing data formats, period slicing, SVG output, and chart parameters.

The library is data-agnostic - it doesn't store or fetch data. Your application manages the data source, and timeseries-sparklines handles the rendering.

## Use Cases

Use `timeseries-sparklines` when your backend, API, or Agentic workflow needs to turn time-series data into lightweight SVG charts without adding frontend charting dependencies.

- **Agentic workflows**: Generate SVG charts from tool results and embed them in chat, dashboards, reports, or generated HTML
- **SSR and backend-rendered apps**: Return ready-to-display SVG from Python backends, or expose it through an API for other stacks
- **Realtime dashboards**: Render many compact sparklines from frequently refreshed data
- **Chart and BI APIs**: Accept slice parameters like `5D`, `1M`, `6M`, or `1Y` and return SVG for downstream consumers
- **Reports, notebooks, and internal tools**: Embed small trend visuals directly where HTML or SVG is supported

**Example from a trading application:**

<div style="display: flex; gap: 16px;">
  <div style="flex: 1;">
    <img src="https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/trading-app-sparklines.png" />
    <p align="center"><em>Dense sparklines for watchlist display</em></p>
  </div>
  <div style="flex: 1;">
    <img src="https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/trading-app-charts.png" />
    <p align="center"><em>Interactive charts with period slicing</em></p>
  </div>
</div>

## System Architecture

The library acts as a server-side rendering harness that transforms time-series data into SVG visualizations. It is designed for applications, APIs, and agentic workflows that need lightweight charts without shipping frontend charting libraries.

**Architecture overview:**

![Timeseries & Sparklines Harness](https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/harness-timeseries-and-sparklines.png)

<center><em>System architecture showing data flow from sources through the rendering harness to consumers (web applications, dashboards, agentic systems, reports, notebooks, and chat interfaces).</em></center>

The harness handles normalization, period-based slicing, coordinate calculation, SVG path generation, and styling - returning production-ready SVG markup that can be embedded anywhere.

## Harness for Charts: Timeseries & Sparklines

Modern AI and Agentic systems often need to communicate trends, not just text. `timeseries-sparklines` acts as a server-side rendering harness for transforming retrieved or computed time-series data into lightweight SVG charts and sparklines.

A typical Agentic workflow:

1. Call a data retrieval tool to fetch raw time-series data from a database, API, cache, or vector-backed workflow in JSON, JSONB, or another supported format.
2. Call `timeseries-sparklines` as a backend rendering tool with the period parameter (`5D`, `1M`, `6M`, `1Y`, or custom timedelta) - the library handles the slicing internally.
3. Embed the returned SVG into a dashboard, generated HTML view, report, notebook, or chat interface.

Because the output is lightweight SVG text, the tool response can be cached, streamed, embedded, and rendered natively anywhere SVG/HTML is supported. Since SVG is text-based markup, it can also be passed through LLM workflows as lightweight visual context when needed.

**Example:**
```python
# Your backend
@app.post("/sparkline-raw")
async def get_sparkline(request: SparklineRequest):
    # Step 1: Fetch from YOUR database
    data = await db.fetch_price_history(symbol="AAPL")

    # Step 2: Render with timeseries-sparklines
    svg = renderer.render(data, color_by_open=request.color_by_open)

    # Step 3: Return SVG
    return Response(content=svg, media_type="image/svg+xml")
```

## What you get

- **Sparkline rendering** - Compact sparkline charts for inline display
- **Interactive charts** - Full time series charts with axis labels and grid lines
- **Configurable styling** - Customizable colors, dimensions, and formatting
- **Data normalization** - Accepts 6+ formats automatically - no preprocessing
- **Period slicing** - Auto-filters to trading days based on period selection
- **Segment coloring** - Color by open price automatically for trend visualization
- **REST API server** - FastAPI-powered service for remote rendering
- **Zero dependencies** - Pure Python - no heavy charting libraries

## Install

```bash
pip install timeseries-sparklines
```

For the REST API server:

```bash
pip install "timeseries-sparklines[api]"
```

## Quick example

### Sparkline Example

```python
from timeseries_svg import SparklineRenderer

data = [
    {"d": "2024-01-01", "c": 100.0},
    {"d": "2024-01-02", "c": 102.5},
    {"d": "2024-01-03", "c": 101.2},
    {"d": "2024-01-04", "c": 105.0},
]

renderer = SparklineRenderer(width=96, height=32)
svg = renderer.render(data)
print(svg)  # Returns SVG string
```

### Chart Example

```python
from timeseries_svg import TimeSeriesChartRenderer

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

The library automatically normalizes various input formats:

### List of Dicts (Standard)
```python
data = [
    {"d": "2024-01-01", "c": 100.0},
    {"d": "2024-01-02", "c": 102.5},
]
```

### List of Lists
```python
data = [
    ["2024-01-01", 100.0],
    ["2024-01-02", 102.5],
]
```

### Dict with Date Keys
```python
data = {
    "2024-01-01": 100.0,
    "2024-01-02": 102.5,
}
```

### Simple Value List
```python
data = [100.0, 102.5, 101.2]
# Dates auto-generated as "day-0", "day-1", etc.
```

### Custom Keys
```python
data = [
    {"date": "2024-01-01", "price": 100.0},
    {"date": "2024-01-02", "price": 102.5},
]
svg = renderer.render(data, date_key="date", value_key="price")
```

## REST API Server

The package includes a FastAPI-powered REST API server for remote rendering:

```bash
# Install with API dependencies
pip install "timeseries-sparklines[api]"

# Run the server
timeseries-server
```

The server starts on `http://0.0.0.0:9300` with endpoints:
- `POST /sparkline-raw` - Render sparkline from JSON data
- `POST /chart-raw` - Render chart from JSON data
- `GET /health` - Health check endpoint

## Value Proposition

**Without timeseries-sparklines, you'd need to:**
- Write SVG rendering code (calculate coordinates, scaling, paths)
- Normalize multiple data formats yourself
- Implement period-based slicing logic
- Calculate proper margins, axis labels, grid lines
- Handle date formatting for different periods
- Implement segment coloring logic

**With timeseries-sparklines:**
```python
# One line to render
svg = renderer.render(data, period="1M", color_by_open=True)
```

It's a rendering engine - you provide raw data, it gives you production-ready SVG. Focus on your application logic, not SVG math.

## Summary

**timeseries-sparklines** is a lightweight, pure Python library for rendering time series data as SVG charts and sparklines.

It's designed for applications that need fast, lightweight visualizations without the overhead of heavy charting libraries. The library accepts multiple data formats automatically, handles scaling and coordinate calculations, and produces responsive SVGs that work seamlessly in web applications.

For applications that need more advanced visualizations (interactive tooltips, zooming, etc.), this library can be combined with other charting libraries. For most use cases where simple, clean visualizations are needed, timeseries-sparklines provides everything required with zero dependencies.

## Links

- [GitHub Repository](https://github.com/vrraj/timeseries-sparklines)
- [PyPI Package](https://pypi.org/project/timeseries-sparklines/)
- [Full README](https://github.com/vrraj/timeseries-sparklines#readme)
- [API Reference](api-reference.html)
- [Deployment Guide](DEPLOYMENT.html)
- [Usage Guide](usage-guide.html)
