# Release Notes

## Version 0.1.0 — Initial Public Release

### Overview

`timeseries-sparklines` is a lightweight server-side SVG rendering engine for sparklines, bar charts, and slicable time-series charts. It accepts time-series data from application-managed sources and returns deterministic SVG markup for SSR applications, dashboards, APIs, reports, notebooks, and agentic workflows.

This is the first public release. The complete API surface is documented in [docs/api-reference.md](https://vrraj.github.io/timeseries-sparklines/api-reference.html).

---

## Core Capabilities

### Sparkline Rendering
- `SparklineRenderer` class for compact sparkline, trend line, and mini chart generation
- Configurable dimensions, stroke width, and colors
- Segment coloring by open price for trend visualization
- Baseline reference line support
- Responsive SVG output with CSS scaling

### Chart Rendering
- `TimeSeriesChartRenderer` class for SVG time-series charts
- `BarChartRenderer` class for vertical bar charts
- Period-based slicing (5D, 1W, 2W, 1M, 3M, 6M, 1Y, or custom timedelta)
- Automatic X-axis tick generation based on period
- Configurable styling (colors, margins, grid lines, axis labels)
- Chart title support with adjustable positioning
- Configurable bar width and colors for bar charts

### Data Normalization
- Accepts 6+ input formats automatically
- List of values (dates auto-generated)
- List of dicts with `d`/`c` keys (date/close)
- List of dicts with `d`/`v` keys (date/value)
- List of dicts with custom keys (date_key, value_key)
- List of lists (date, value pairs)
- Dict with date keys
- Auto-detection of common key aliases (`c`, `v`, `value`)

### REST Service
- FastAPI-powered REST API for remote rendering
- Endpoints for sparkline, line chart, and bar chart rendering
- Interactive test UI for testing data formats, period slicing, SVG output, and chart parameters
- Period filter support with custom timedelta
- Pydantic models for type-safe request/response handling

### System Architecture
- Pure rendering engine - data-agnostic design
- Server-side SVG generation (no frontend chart libraries)
- SSR-friendly architecture for backend-rendered applications
- Backend rendering harness pattern for agentic workflows
- REST service or in-process usage patterns

---

## Documentation Structure

- **[README.md](https://github.com/vrraj/timeseries-sparklines#readme)** — Quick start and high-level overview
- **[docs/index.md](https://vrraj.github.io/timeseries-sparklines/)** — Project documentation with examples
- **[docs/api-reference.md](https://vrraj.github.io/timeseries-sparklines/api-reference.html)** — Complete method signatures and parameters
- **[docs/usage-guide.md](https://vrraj.github.io/timeseries-sparklines/usage-guide.html)** — Data input formats and examples
- **[docs/DEPLOYMENT.md](https://vrraj.github.io/timeseries-sparklines/DEPLOYMENT.html)** — Installation and deployment guide
- **[ReleaseNotes.md](https://github.com/vrraj/timeseries-sparklines/blob/main/ReleaseNotes.md)** — Version history

---

## Public API Surface

For the complete API reference including all parameters, method signatures, and examples, see [docs/api-reference.md](https://vrraj.github.io/timeseries-sparklines/api-reference.html).

Key examples:

**Sparkline rendering:**
```python
from timeseries_svg import SparklineRenderer

renderer = SparklineRenderer(width=96, height=32)
svg = renderer.render([100, 102.5, 101.2, 105, 103.8])
```

**Bar chart with y-axis label:**
```python
from timeseries_svg import BarChartRenderer

renderer = BarChartRenderer(
    width=760,
    height=320,
    bar_color="#3b82f6",
    y_axis_label="Revenue ($)",
    y_axis_offset=0.1
)
svg = renderer.render(data, period="1M", title="Monthly Revenue")
```

**Line chart with period filtering and y-axis label:**
```python
from timeseries_svg import TimeSeriesChartRenderer

renderer = TimeSeriesChartRenderer(
    width=760,
    height=320,
    y_axis_label="Temperature (°C)",
    y_axis_offset=0.1
)
svg = renderer.render(data, period="6M", title="Temperature Trends")
```

---

## Compatibility

- Python 3.9+
- Pure Python with zero external dependencies for core library
- FastAPI and Uvicorn for REST service (optional)
- Jinja2 for test UI (optional)

---

## Notes

This release establishes the 0.1.0 API contract for `timeseries-sparklines`.

The focus of this release is server-side SVG rendering for sparklines, bar charts, and slicable time-series charts in SSR applications, dashboards, APIs, and agentic workflows. The library is designed as a rendering engine that accepts application-provided time-series data and returns SVG markup.

Key design decisions:
- Data-agnostic: Does not fetch, store, or poll data
- Server-side rendering: Browser displays returned SVG without a frontend chart runtime
- Flexible input: Auto-normalizes 6+ JSONB formats
- Period-based filtering: Time windows for slicable charts
- SVG output: Embeddable vector markup for web pages, reports, notebooks, and generated HTML

Backward compatibility will be maintained within the 0.1.x series.
