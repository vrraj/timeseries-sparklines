# timeseries-sparklines

[![CI](https://github.com/vrraj/timeseries-sparklines/actions/workflows/ci.yml/badge.svg)](https://github.com/vrraj/timeseries-sparklines/actions)
[![PyPI - Version](https://img.shields.io/pypi/v/timeseries-sparklines?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/timeseries-sparklines/)
[![GitHub Release](https://img.shields.io/github/v/release/vrraj/timeseries-sparklines?label=github%20release&color=orange&logo=github)](https://github.com/vrraj/timeseries-sparklines/releases)



Need backend-rendered **sparklines**, **trend lines**, **mini charts**, **bar charts**, or **slicable time-series charts**?

>`timeseries-sparklines` turns time-series data into deterministic SVG markup for SSR applications, dashboards, APIs, and Agentic workflows - no chart initialization, no canvas lifecycle management, and no frontend chart runtime required.

```
pip install timeseries-sparklines
```

Includes an **Interactive Test UI** for testing data formats, period slicing, SVG output, and chart parameters.

## Rendered Examples

<p align="center"><em>Example: an Agentic workflow returning a server-rendered SVG chart inside an LLM response.</em></p>

<p align="center">
  <img src="https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/tool-harness-for-chart-in-llm-response.png" width="88%" />
</p>

<p align="center"><em>Sparklines, bar charts, and slicable SVG time-series charts rendered server-side.</em></p>

<p align="center">
  <img src="https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/sparklines-with-list-of-values.png" width="30%" />
  <img src="https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/bar-chart-with-list-of-dicts.png" width="30%" />
  <img src="https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/chart-with-dict-date-value.png" width="30%" />
</p>

### Trading Dashboard Preview

<p align="center"><em>Example: backend-rendered sparklines and slicable SVG charts inside a trading dashboard.</em></p>

<p align="center">
  <img src="https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/trading-app-sparklines.png" width="48%" />
  <img src="https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/trading-app-charts.png" width="48%" />
</p>

**[Quick Start →](#install)**

## Use Cases

Use `timeseries-sparklines` when your backend, API, or Agentic workflow needs to turn time-series data into lightweight SVG charts without adding frontend charting dependencies.

- **Agentic workflows**: Generate SVG charts from tool results and embed them in chat, dashboards, reports, or generated HTML
- **SSR and backend-rendered apps**: Return ready-to-display SVG from Python backends, or expose it through an API for other stacks
- **Operational dashboards**: Render compact sparklines, trend lines, and mini charts for periodically refreshed data
- **Chart and BI APIs**: Accept slice parameters like `5D`, `1M`, `6M`, or `1Y` and return SVG for downstream consumers
- **Reports, notebooks, and internal tools**: Embed small trend visuals directly where HTML or SVG is supported

## System Architecture

The library acts as a server-side rendering harness that transforms time-series data into SVG visualizations.

**Architecture overview:**

<center><em>System architecture showing data flow from sources through the rendering harness to downstream consumers.</em></center>

![Timeseries & Sparklines Harness](https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/harness-timeseries-and-sparklines.png)

The harness handles normalization, slicing, coordinate calculation, and SVG generation - returning production-ready SVG markup.

## Harness for Charts: Timeseries & Sparklines

`timeseries-sparklines` can act as a backend rendering harness inside Agentic workflows, APIs, dashboards, and SSR applications.

A typical workflow:

1. Retrieve time-series data from a database, API, cache, or tool
2. Render a sparkline or chart with a selected period (`5D`, `1M`, `6M`, `1Y`, etc.)
3. Return SVG for embedding into dashboards, reports, notebooks, or chat interfaces

Because the output is lightweight SVG text, it can be cached, streamed, embedded, and passed through LLM workflows when needed.

## What you get

- **Python rendering library** for programmatic sparkline and chart generation
- **Flexible data input** - Accepts 6+ Python/JSON time-series formats automatically
- **Sparkline rendering** - Compact sparklines, trend lines, and mini charts for inline display
- **Bar charts** - Vertical bar charts for time-series data with configurable bar width and colors
- **Time-series charts** - SVG charts with axis labels, grid lines, and period-based formatting
- **Period-based slicing** - Auto-filters data by time windows (5D, 1W, 2W, 1M, 3M, 6M, 1Y, or custom timedelta)
- **Segment coloring** - Color segments by open price for trend visualization
- **REST API server** - FastAPI-powered service for remote rendering
- **Zero external dependencies** - Pure Python, no heavy plotting libraries required
- **Test UI** - Interactive test page for rendering behavior and parameter tuning

## Install

```bash
pip install timeseries-sparklines
```

Or install with REST API server:

```bash
pip install "timeseries-sparklines[api]"
```

Links:

- **PyPI:** https://pypi.org/project/timeseries-sparklines/
- **GitHub:** https://github.com/vrraj/timeseries-sparklines
- **API Documentation:** https://vrraj.github.io/timeseries-sparklines/

## Quick Start

### Option A: Use directly in Python

*For Python applications (most common)*

```bash
pip install timeseries-sparklines
```

### Sparkline Example

```python
from timeseries_svg import SparklineRenderer

# Input data can be in various formats
data = [
    {"d": "2024-01-01", "v": 100.0},
    {"d": "2024-01-02", "v": 102.5},
    {"d": "2024-01-03", "v": 101.2},
    {"d": "2024-01-04", "v": 105.0},
]

renderer = SparklineRenderer(width=96, height=32)
svg = renderer.render(data)
print(svg)  # Returns SVG string
```

### Time Series Chart Example

```python
from timeseries_svg import TimeSeriesChartRenderer

# Historical price data
data = [
    {"d": "2024-01-01", "v": 150.0},
    {"d": "2024-01-02", "v": 152.5},
    {"d": "2024-01-03", "v": 151.0},
    {"d": "2024-01-04", "v": 155.0},
    {"d": "2024-01-05", "v": 158.0},
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

# Temperature data by month
data = [
    {"d": "2024-01-01", "v": 65.0},
    {"d": "2024-02-01", "v": 68.0},
    {"d": "2024-03-01", "v": 72.0},
    {"d": "2024-04-01", "v": 75.0},
    {"d": "2024-05-01", "v": 80.0},
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

## Usage Patterns

### Direct Python Library Usage
Use the renderers directly in your Python code for programmatic SVG generation. Ideal for:
- Batch rendering of time-series data
- Report generation
- Static site generation
- Data pipelines

```python
from timeseries_svg import SparklineRenderer, TimeSeriesChartRenderer

# Sparkline
sparkline_renderer = SparklineRenderer(width=200, height=64)
sparkline_svg = sparkline_renderer.render([100.0, 102.5, 101.2, 105.0])

# Chart
chart_renderer = TimeSeriesChartRenderer()
chart_svg = chart_renderer.render(data, period="1M", title="Price History")
```

### REST API Server Usage
Run the included FastAPI server for remote rendering. Ideal for:
- Microservices architecture
- Multi-application environments that need shared SVG rendering
- Remote deployments
- Service-oriented integration

```bash
pip install "timeseries-sparklines[api]"
timeseries-server
```

The server starts on `http://0.0.0.0:9300` with endpoints:
- `POST /sparkline-raw` - Render sparkline from JSON data
- `POST /chart-raw` - Render chart from JSON data
- `GET /test-charts` - Interactive test UI
- `GET /health` - Health check

## Interactive Test UI

The GitHub repository includes a FastAPI-powered **Test UI** for testing rendering behavior, inspecting SVG output, and tuning chart parameters.

It acts as an interactive experimentation environment. You can test different data formats, adjust period filters, customize chart styling, and iteratively refine rendering settings using the included UI.

This helps you visualize how different data formats are normalized and how charts are rendered before using the settings in production.

<div style="display: flex; gap: 16px;">
  <div style="flex: 1;">
    <p align="center"><em>Sparkline rendering with list of values format</em></p>
    <img src="https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/sparklines-with-list-of-values.png" />
  </div>
  <div style="flex: 1;">
    <p align="center"><em>Chart rendering with dict date/value format and period slicing</em></p>
    <img src="https://raw.githubusercontent.com/vrraj/timeseries-sparklines/main/images/chart-with-dict-date-value.png" />
  </div>
</div>

Run locally:

```bash
git clone https://github.com/vrraj/timeseries-sparklines.git
cd timeseries-sparklines
pip install "timeseries-sparklines[api]"
timeseries-server
```

Open:

```text
http://localhost:9300/test-charts
```

## Why Server-Side SVG?

### Backend Rendering Advantages

- **Zero frontend chart runtime**: No frontend chart dependency, no chart-specific bundle weight, and no browser-side chart initialization.
- **SSR-friendly output**: SVG can be embedded directly in HTML generated by Django, FastAPI/Jinja, Flask, Next.js, Laravel, Rails, or HTMX-style applications.
- **Built-in normalization**: The renderer maps raw values into SVG coordinates by calculating local min/max ranges, viewport dimensions, margins, and path geometry.
- **Consistent visual output**: Rendering happens in one controlled backend layer, so the same input data produces the same SVG markup across clients.

### Slice, Scale, Draw, Respond

Your backend can expose chart views instead of raw chart logic. For example, you could implement an endpoint like:

```http
GET /chart/AAPL?period=6M&theme=dark
```

This would fetch data for AAPL, render it with the specified period, and return SVG - all handled by your backend using the timeseries-sparklines renderer.

## Data Input Formats

The library automatically normalizes various input formats. Use the format that best matches your data source:

### List of Dicts (Standard Format)
Recommended for most use cases. Uses `d` for date and `v` for value.

```python
data = [
    {"d": "2024-01-01", "v": 100.0},
    {"d": "2024-01-02", "v": 102.5},
    {"d": "2024-01-03", "v": 101.2},
    {"d": "2024-01-04", "v": 105.0},
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
        {"d": "2024-01-01", "v": 100.0},
        {"d": "2024-01-02", "v": 102.5},
    ]
}

# The library extracts the array automatically
```

## Configuration

### Sparkline Renderer

```python
renderer = SparklineRenderer(
    width=96,              # SVG width in pixels
    height=32,             # SVG height in pixels
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



## Integration with Web Frameworks

### FastAPI Example

```python
from fastapi import FastAPI, Response
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

### Data Ownership

`timeseries-sparklines` is a rendering service, not a data service. Your application controls:

- Data fetching from databases, APIs, caches, or other systems
- Polling frequency, retries, and error handling
- Caching and business logic
- When to call the renderer and refresh the SVG

Typical backend pattern:

```python
@app.get("/api/stocks/sparkline")
async def sparkline_api(symbol: str, period: str = "5D"):
    data = await get_price_history(symbol, period)
    svg = renderer.render(data, color_by_open=True)
    return Response(content=svg, media_type="image/svg+xml")
```

## Frontend Integration Patterns

For frequently refreshed sparklines, server-side SVG rendering works best when updates are periodic, cacheable, and backed by server-side caching rather than sub-second.

For high-frequency streaming views, a hybrid approach is usually more efficient:

- Use `timeseries-sparklines` for the initial sparkline render or SSR response
- Batch multiple sparklines server-side when rendering many charts on one page, such as 50 symbols in a watchlist
- Cache rendered SVGs or source data on the backend when multiple users request the same view
- Use WebSockets or incremental frontend updates for live changes
- Pause polling when browser tabs are inactive and refresh the full sparkline on wake-up or focus

This pattern works best when:

- Update frequency is moderate, such as 30-60 seconds for sparklines
- Many similar charts can share cached data or rendered SVG output
- Multiple sparklines can be batched into a single backend response
- The frontend mainly displays SVG and does not need heavy chart interaction

Recommended pattern:

1. **Render charts or sparklines from backend data**
   - Your backend fetches or receives the latest time-series data
   - `timeseries-sparklines` renders the SVG
   - The frontend replaces the SVG markup in the target container

2. **Render larger charts on demand**
   - User selects a symbol, metric, chart, or period
   - Frontend requests a chart with a period such as `5D`, `1M`, `3M`, `6M`, or `1Y`
   - The backend returns a sliced SVG chart

**Example: Batch multiple sparklines in one request**

```javascript
// Batch fetch multiple sparklines
async function fetchSparklines(symbols) {
  const response = await fetch('/api/sparklines', {
    method: 'POST',
    body: JSON.stringify({ symbols, period: '5D' })
  });
  const data = await response.json();
  // data.svgs = { 'AAPL': '<svg>...', 'GOOGL': '<svg>...' }
  Object.entries(data.svgs).forEach(([symbol, svg]) => {
    document.getElementById(`sparkline-${symbol}`).innerHTML = svg;
  });
}

// Poll with visibility API to pause when tab is inactive
let pollInterval;
function startPolling(symbols) {
  pollInterval = setInterval(() => {
    if (!document.hidden) {
      fetchSparklines(symbols);
    }
  }, 30000); // 30 seconds
}
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) fetchSparklines(symbols); // Refresh on wake-up
});
```

Best practice: set a minimum height on the target container to avoid layout shifts when SVG is injected.

```css
.sparkline-container {
  min-height: 64px;
}

.chart-container {
  min-height: 320px;
}
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
