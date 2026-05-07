# timeseries-sparklines

[![PyPI - Version](https://img.shields.io/pypi/v/timeseries-sparklines?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/timeseries-sparklines/)
[![GitHub Release](https://img.shields.io/github/v/release/vrraj/timeseries-sparklines?label=github%20release&color=orange&logo=github)](https://github.com/vrraj/timeseries-sparklines/releases)



> **Interactive Test UI:**  
> The package includes a FastAPI-powered **Test UI** for testing rendering behavior, inspecting SVG output, and tuning chart parameters. Run `timeseries-server` and visit `http://localhost:9300/test-charts`.

Need to add **real-time sparklines** or **slicable time-series charts** to your application, dashboard, or Agentic systems?

`timeseries-sparklines` is a lightweight server-side SVG rendering engine for **dense time-series sparklines** and **interactive charts** that can be sliced by days, weeks, months, years, or custom time windows.

It is designed for SSR-first applications, dashboards, watchlists, Agentic systems, and real-time monitoring interfaces where many lightweight charts need to be rendered without shipping a frontend charting library.

### Harness for Charts: Timeseries & Sparklines

Modern AI and Agentic systems often need to communicate trends, not just text. `timeseries-sparklines` acts as a server-side rendering harness for transforming retrieved or computed time-series data into lightweight SVG charts and sparklines.

A typical Agentic workflow:

1. Call a data retrieval tool to fetch raw time-series data from a database, API, cache, or vector-backed workflow in JSON, JSONB, or another supported format.
2. Call `timeseries-sparklines` as a backend rendering tool with the period parameter (`5D`, `1M`, `6M`, `1Y`, or custom timedelta) - the library handles the slicing internally.
3. Embed the returned SVG into a dashboard, generated HTML view, report, notebook, or chat interface.

Because the output is lightweight SVG text, the tool response can be cached, streamed, embedded, and rendered natively anywhere SVG/HTML is supported. Since SVG is text-based markup, it can also be passed through LLM workflows as lightweight visual context when needed.

**[Quick Start →](#install)**

## Why this exists

Applications and Agentic systems often need lightweight time-series visualizations without pulling chart logic into the frontend or orchestration layer. Traditional frontend charting libraries can increase bundle size, require browser-side initialization, and add complexity when all you need is a small, deterministic trend visualization.

> `timeseries-sparklines` gives you a **server-side rendering engine** that produces deterministic SVG markup. The browser simply displays the returned SVG - **NO** chart initialization, **NO** canvas lifecycle management, and **NO** frontend chart runtime required.

This becomes especially useful in:
- **Agentic systems** where orchestration layers need a backend charting tool
- **SSR applications** where HTML is generated on the server
- **Dense dashboards** where many sparklines are rendered on the same page
- **Real-time watchlists** where charts update frequently
- **Generated reports, notebooks, and HTML views** where SVG can be embedded directly

Typical flow:

```text
Data Source → Backend / Agent Tool Call → timeseries-sparklines → SVG → UI / Report / Browser / Agent Response
```

## Data Flow

The library is data-agnostic - it does not fetch, store, or poll data. Your application, API layer, or Agentic workflow manages the data source and calls `timeseries-sparklines` as the rendering harness.

Typical flow:

```text
Data Sources → timeseries-sparklines Harness → SVG Response → Consumers
```

Where:

- **Data Sources**: Database, external APIs, caches, or internal systems
- **timeseries-sparklines Harness**: normalization, slicing, scaling, SVG path geometry, coordinate calculation, and SVG wrapping
- **SVG Response**: raw SVG text or JSON payload containing SVG markup
- **Consumers**: Agentic systems, web applications, dashboards, reports, notebooks, or chat interfaces

The frontend simply renders the returned SVG markup - no browser-side chart initialization, canvas lifecycle management, or frontend chart runtime required.

<center><em>Figure: Harness for Charts: Timeseries & Sparklines — The server-side engine for Agentic Workflows and SSR visualization.</em></center>

## What you get

- **Python rendering library** for programmatic sparkline and chart generation
- **Flexible data input** - Accepts 6+ Python/JSON time-series formats automatically
- **Sparkline rendering** - Compact sparkline charts for inline display
- **Time series charts** - SVG charts with axis labels, grid lines, and period-based formatting
- **Period-based slicing** - Auto-filters data by time windows (5D, 1W, 2W, 1M, 3M, 6M, 1Y, or custom timedelta)
- **Segment coloring** - Color segments by open price for trend visualization
- **REST API server** - FastAPI-powered service for remote rendering
- **Zero external dependencies** - Pure Python, no heavy plotting libraries required
- **Test UI** - Interactive test page for rendering behavior and parameter tuning

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

## Usage Patterns

### Direct Python Library Usage
Use the renderers directly in your Python code for programmatic SVG generation. Ideal for:
- Batch processing of time-series data
- Report generation
- Static site generation
- Data pipelines

```python
from timeseries_sparklines import SparklineRenderer, TimeSeriesChartRenderer

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
- Multi-application environments
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

### Web Framework Integration
Integrate directly into FastAPI, Flask, Django, or any Python web framework. Ideal for:
- SSR applications
- API-driven dashboards
- Real-time watchlists
- Custom chart endpoints

```python
# FastAPI
from fastapi import FastAPI, Response
from timeseries_sparklines import SparklineRenderer

app = FastAPI()
renderer = SparklineRenderer()

@app.get("/sparkline/{symbol}")
async def get_sparkline(symbol: str):
    data = await fetch_price_data(symbol)
    svg = renderer.render(data)
    return Response(content=svg, media_type="image/svg+xml")
```

### Backend Tool Harness for AI / Agentic Systems
Use as a backend rendering tool inside AI pipelines and agent systems. Ideal for:
- LLM-generated visualizations
- Agentic dashboard updates
- Computed metric display
- Embedded chart generation

```python
# In an AI / agentic tool pipeline
data = agent.retrieve_time_series(symbol="AAPL", period="6M")
svg = renderer.render(data, period="6M", title="AAPL 6M History")
agent.embed_in_dashboard(svg)
```

## Why Server-Side SVG?

### Backend Rendering Advantages

- **Zero frontend chart runtime**: No frontend chart dependency, no chart-specific bundle weight, and no browser-side chart initialization.
- **SSR-friendly output**: SVG can be embedded directly in HTML generated by Django, FastAPI/Jinja, Flask, Next.js, Laravel, Rails, or HTMX-style applications.
- **Built-in normalization**: The renderer maps raw values into SVG coordinates by calculating local min/max ranges, viewport dimensions, margins, and path geometry.
- **Consistent visual output**: Rendering happens in one controlled backend layer, so the same input data produces the same SVG markup across clients.

### Slice, Scale, Draw, Respond

Your backend can expose chart views instead of raw chart logic. For example:

```http
GET /chart/AAPL?period=6M&theme=dark
```

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
from timeseries_sparklines import SparklineRenderer

# Input data can be in various formats
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

### Time Series Chart Example

```python
from timeseries_sparklines import TimeSeriesChartRenderer

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
from timeseries_sparklines import normalize_timeseries_data, extract_values, extract_dates

normalized = normalize_timeseries_data(data)
values = extract_values(normalized)
dates = extract_dates(normalized)
```

## Use Cases

- **Financial dashboards**: Stock price sparklines and historical charts
- **AI and agentic systems**: Generate embeddable SVG visualizations from retrieved or computed time-series data
- **Analytics platforms**: Time series metrics and trends
- **Trading applications**: Price history and technical indicators
- **Web and SSR applications**: Lightweight SVG charts without heavy frontend chart dependencies
- **IoT monitoring**: Real-time sensor data visualization

## Additional AI / Agentic Integration Notes

`timeseries-sparklines` can also be used as a backend rendering utility inside AI pipelines and agent systems.

An orchestration layer or LLM can:

- Retrieve time-series data
- Compute or transform metrics
- Call the renderer
- Embed SVG output directly into dashboards, reports, chats, generated HTML, or monitoring interfaces

Because the output is deterministic SVG markup, charts can be streamed, cached, embedded, and composed without frontend chart dependencies.

## Integration with Web Frameworks

### FastAPI Example

```python
from fastapi import FastAPI, Response
from timeseries_sparklines import SparklineRenderer

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
from timeseries_sparklines import TimeSeriesChartRenderer

app = Flask(__name__)
renderer = TimeSeriesChartRenderer()

@app.route("/chart/<symbol>")
def chart(symbol):
    data = fetch_historical_data(symbol)
    svg = renderer.render(data, period="1M")
    return Response(svg, mimetype="image/svg+xml")
```

### Data Polling Architecture

**Important: timeseries-sparklines does NOT handle data fetching or polling.** It's a pure rendering engine. Your application manages:

- **Data fetching** (database, external API, cache, etc.)
- **Polling logic** (intervals, error handling, retries)
- **Caching** (reduce load on data sources)
- **Business logic** (data transformation, filtering)

**Complete Data Flow:**

```
┌─────────────────────────────────────────────────────────────────┐
│                        Your Application                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. Frontend polls YOUR data API every N seconds                │
│     → fetch('/api/price-history?symbols=AAPL&period=5D')         │
│                                                                   │
│  2. YOUR backend fetches from YOUR data source                  │
│     → PostgreSQL, external API, Redis cache, etc.                │
│                                                                   │
│  3. YOUR backend sends data to timeseries-sparklines             │
│     → renderer.render(data)                                      │
│                                                                   │
│  4. timeseries-sparklines returns SVG                            │
│     → YOUR backend returns SVG to frontend                       │
│                                                                   │
│  5. Frontend displays SVG                                        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Backend Integration Example:**

```python
from fastapi import FastAPI, Response
from timeseries_sparklines import SparklineRenderer

app = FastAPI()
renderer = SparklineRenderer()

@app.get("/api/stocks/sparkline")
async def sparkline_api(symbols: str, period: str = "5D", db: Session = Depends(get_db)):
    # Step 1: YOUR application fetches data from YOUR source
    data = await get_price_history_from_db(db, symbols, period)
    
    # Step 2: Render with timeseries-sparklines
    svg = renderer.render(data, color_by_open=True)
    
    # Step 3: Return SVG
    return Response(content=svg, media_type="image/svg+xml")
```

**Frontend Polling Example:**

```javascript
// Poll YOUR backend for data + SVG
setInterval(async () => {
    const response = await fetch('/api/stocks/sparkline?symbols=AAPL&period=5D');
    const svg = await response.text();
    document.getElementById('sparkline-AAPL').innerHTML = svg;
}, 30000); // Poll every 30 seconds
```

**Alternative: Separate Data and Rendering**

```javascript
// Poll for data separately
setInterval(async () => {
    const response = await fetch('/api/price-history?symbols=AAPL&period=5D');
    const data = await response.json();
    
    // Send data to timeseries-sparklines API
    const sparklineResponse = await fetch('http://localhost:9300/sparkline-raw', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: data, color_by_open: true })
    });
    
    const svg = await sparklineResponse.text();
    document.getElementById('sparkline-AAPL').innerHTML = svg;
}, 30000);
```

**Key Points:**
- timeseries-sparklines is a **rendering service**, not a data service
- You control polling frequency, error handling, retries
- You implement caching strategies for your data
- You decide when to refresh (on user action, on schedule, on WebSocket event)

## Frontend Integration Pattern

**Recommended Architecture:**

1. **Sparkline Polling (Real-time Updates)**
   - Poll sparkline endpoint every N seconds (configurable, e.g., 60s)
   - Update inline sparkline SVGs in the DOM
   - Minimal bandwidth - only SVG strings

2. **Chart on Click (On-Demand)**
   - User clicks sparkline → opens modal/overlay
   - Fetch full chart with selected period (5D, 1M, 3M, 6M, 1Y)
   - Auto-slices data based on period (no manual filtering needed)

**Best Practice: Prevent Layout Shifts**

When injecting SVG via `innerHTML`, define a `min-height` on your container div that matches your renderer height to prevent layout shifts:

```css
.sparkline-container {
  min-height: 64px; /* Matches SparklineRenderer height */
}

.chart-container {
  min-height: 320px; /* Matches TimeSeriesChartRenderer height */
}
```

**JavaScript Example:**

```javascript
// Poll sparklines every 60 seconds (configurable)
const POLL_INTERVAL_MS = 60000;

async function pollSparklines() {
  const symbols = ['AAPL', 'NVDA', 'TSLA', 'COIN', 'MSFT'];
  
  for (const symbol of symbols) {
    try {
      const response = await fetch('/sparkline-raw', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          data: sparklineData[symbol],
          color_by_open: true  // optional: color segments by open price
        })
      });
      
      if (response.ok) {
        const svg = await response.text();
        const container = document.getElementById(`sparkline-${symbol}`);
        if (container) container.innerHTML = svg;
      }
    } catch (error) {
      console.error(`Failed to update sparkline for ${symbol}:`, error);
    }
  }
}

// Start polling
setInterval(pollSparklines, POLL_INTERVAL_MS);
pollSparklines(); // Initial load

// Show chart on sparkline click
async function showChart(symbol, period = '1M') {
  const modal = document.getElementById('chart-modal');
  const modalTitle = document.getElementById('chart-symbol');
  
  modalTitle.textContent = symbol;
  modal.classList.remove('hidden');
  
  try {
    const response = await fetch('/chart-raw', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        data: chartData[symbol],  // Full historical data
        period: period,           // 5D, 1M, 3M, 6M, 1Y
        title: `${symbol} Price History`,
        color_by_open: true       // optional: color segments by open price
      })
    });
    
    if (response.ok) {
      const svg = await response.text();
      document.getElementById('chart-container').innerHTML = svg;
    }
  } catch (error) {
    console.error('Failed to load chart:', error);
  }
}

// Close modal
function closeChart() {
  document.getElementById('chart-modal').classList.add('hidden');
}
```

**HTML Structure:**

```html
<!-- Sparkline table row -->
<tr>
  <td>AAPL</td>
  <td>
    <div id="sparkline-AAPL" onclick="showChart('AAPL')"></div>
  </td>
  <td>150.25</td>
</tr>

<!-- Chart modal -->
<div id="chart-modal" class="modal hidden">
  <div class="modal-content">
    <div class="modal-header">
      <span id="chart-symbol"></span>
      <button onclick="closeChart()">×</button>
    </div>
    <div class="tabs">
      <button onclick="showChart('AAPL', '5D')">5D</button>
      <button onclick="showChart('AAPL', '1M')" class="active">1M</button>
      <button onclick="showChart('AAPL', '3M')">3M</button>
      <button onclick="showChart('AAPL', '6M')">6M</button>
      <button onclick="showChart('AAPL', '1Y')">1Y</button>
    </div>
    <div id="chart-container"></div>
  </div>
</div>
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
