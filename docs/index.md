---
layout: default
title: "Timeseries SVG: Time Series Visualization"
description: "Server-side SVG rendering harness for sparklines, trend lines, mini charts, and slicable time-series charts for dashboards, SSR applications, and Agentic workflows."
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

Need to add **sparklines**, **trend lines**, **mini charts**, **bar charts**, or **slicable time-series charts** to your application, dashboard, or Agentic systems?

`timeseries-sparklines` is a lightweight server-side SVG rendering engine for **dense time-series sparklines** and **SVG charts** that can be sliced by days, weeks, months, years, or custom time windows. It produces deterministic SVG markup that the browser can simply display - no chart initialization, no canvas lifecycle management, and no frontend chart runtime required.

```
pip install timeseries-sparklines
```

Includes an **Interactive Test UI** for testing data formats, period slicing, SVG output, and chart parameters.

The library is data-agnostic - it does not fetch, store, or poll data. Your application manages the data source, and `timeseries-sparklines` handles normalization, slicing, coordinate calculation, and SVG rendering.

## Use Cases

Use `timeseries-sparklines` when your backend, API, or Agentic workflow needs to turn time-series data into lightweight SVG charts without adding frontend charting dependencies.

- **Agentic workflows**: Generate SVG charts from tool results and embed them in chat, dashboards, reports, or generated HTML
- **SSR and backend-rendered apps**: Return ready-to-display SVG from Python backends, or expose it through an API for other stacks
- **Operational dashboards**: Render compact sparklines, trend lines, and mini charts for periodically refreshed data
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

The library acts as a server-side rendering harness that transforms time-series data into lightweight SVG visualizations for applications, APIs, dashboards, SSR workflows, and Agentic systems.

![Timeseries & Sparklines Harness](https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/harness-timeseries-and-sparklines.png)

<center><em>System architecture showing data flow from sources through the rendering harness to downstream consumers.</em></center>

The harness handles normalization, slicing, coordinate calculation, and SVG generation - returning production-ready SVG markup.

## Harness for Charts: Timeseries & Sparklines

`timeseries-sparklines` can act as a backend rendering harness inside Agentic workflows, APIs, dashboards, and SSR applications.

A typical workflow:

1. Retrieve time-series data from a database, API, cache, or tool
2. Render a sparkline or chart with a selected period (`5D`, `1M`, `6M`, `1Y`, etc.)
3. Return SVG for embedding into dashboards, reports, notebooks, or chat interfaces

Because the output is lightweight SVG text, it can be cached, streamed, embedded, and passed through LLM workflows when needed.

## What you get

- **Sparkline rendering** - Compact sparklines, trend lines, and mini charts for inline display
- **Bar charts** - Vertical bar charts for time-series data with configurable bar width and colors
- **Time-series charts** - SVG charts with axis labels, grid lines, and period-based formatting
- **Configurable styling** - Customizable colors, dimensions, and formatting
- **Data normalization** - Accepts multiple input formats automatically
- **Period slicing** - Auto-filters to trading days based on period selection
- **Segment coloring** - Optional color-by-open rendering for trend visualization
- **REST API server** - FastAPI-powered rendering service
- **Zero frontend chart runtime** - Browser displays returned SVG directly

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
print(svg)  # Returns SVG string
```

**With custom y-axis label:**
```python
renderer = TimeSeriesChartRenderer(width=760, height=320, y_axis_label="$")
svg = renderer.render(data, period="5D", title="AAPL Price History")
```

### Bar Chart Example

```python
from timeseries_svg import BarChartRenderer

data = [
    {"d": "2024-01-01", "c": 65.0},
    {"d": "2024-02-01", "c": 68.0},
    {"d": "2024-03-01", "c": 72.0},
    {"d": "2024-04-01", "c": 75.0},
    {"d": "2024-05-01", "c": 80.0},
]

renderer = BarChartRenderer(width=760, height=320)
svg = renderer.render(data, period="1Y", title="Temperature by Month")
print(svg)  # Returns SVG string
```

**With custom y-axis label:**
```python
renderer = BarChartRenderer(width=760, height=320, y_axis_label="°F")
svg = renderer.render(data, period="1Y", title="Temperature by Month")
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

## Frontend Integration Pattern

For frequently refreshed sparklines, server-side SVG rendering works best when updates are periodic, cacheable, and backed by server-side caching rather than sub-second or tick-level.

For high-frequency streaming views, a hybrid approach is usually more efficient:

- Use `timeseries-sparklines` for the initial sparkline render or SSR response
- Batch multiple sparklines server-side when rendering many charts on one page
- Cache rendered SVGs or source data on the backend when multiple users request the same view
- Use WebSockets or incremental frontend updates for live changes
- Pause polling when browser tabs are inactive and refresh the full sparkline on wake-up or focus

This pattern works best when:

- Update frequency is moderate, such as 30-60 seconds for sparklines
- Many similar charts can share cached data or rendered SVG output
- Multiple sparklines can be batched into a single backend response
- The frontend mainly displays SVG and does not need heavy chart interaction

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

**timeseries-sparklines** is a lightweight server-side SVG rendering engine for sparklines, trend lines, mini charts, and slicable time-series charts.

It is designed for SSR-first applications, periodically refreshed dashboards, APIs, and Agentic systems that need lightweight visualizations without shipping heavy frontend charting libraries.

The library accepts multiple data formats automatically, handles normalization and coordinate calculations, and produces deterministic SVG markup that can be embedded directly into dashboards, reports, notebooks, generated HTML, and chat interfaces.

## Links

- [GitHub Repository](https://github.com/vrraj/timeseries-sparklines)
- [PyPI Package](https://pypi.org/project/timeseries-sparklines/)
- [Full README](https://github.com/vrraj/timeseries-sparklines#readme)
- [API Reference](api-reference.html)
- [Deployment Guide](DEPLOYMENT.html)
- [Usage Guide](usage-guide.html)
