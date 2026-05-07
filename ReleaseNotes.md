# Release Notes

## Version 0.1.0 — Initial Public Release

### Overview

`timeseries-sparklines` is a lightweight server-side SVG rendering engine for time-series data visualization. Accepts JSONB data from any source (periodically refreshed for sparklines or historical data) and produces clean, interactive SVG visualizations for web applications, dashboards, and agentic systems.

This is the first public release. The complete API surface is documented in [docs/api-reference.md](https://vrraj.github.io/timeseries-sparklines/api-reference.html).

---

## Core Capabilities

### Sparkline Rendering
- `SparklineRenderer` class for compact sparkline chart generation
- Configurable dimensions, stroke width, and colors
- Segment coloring by open price for trend visualization
- Baseline reference line support
- Responsive SVG output with CSS scaling

### Chart Rendering
- `TimeSeriesChartRenderer` class for full time-series charts
- Period-based slicing (5D, 1W, 2W, 1M, 3M, 6M, 1Y, or custom timedelta)
- Automatic X-axis tick generation based on period
- Configurable styling (colors, margins, grid lines, axis labels)
- Chart title support with adjustable positioning

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
- Endpoints for sparkline and chart rendering
- Interactive test UI for format experimentation
- Period filter support with custom timedelta
- Pydantic models for type-safe request/response handling

### System Architecture
- Pure rendering engine - data-agnostic design
- Server-side SVG generation (no frontend chart libraries)
- SSR-first architecture for web applications
- Agentic system integration for AI workflows
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

Stable entry points:
- `SparklineRenderer(width, height, stroke_width, baseline_color, up_color, down_color, show_baseline, color_by_open)` — Sparkline chart renderer
- `SparklineRenderer.render(data)` — Render sparkline from data
- `TimeSeriesChartRenderer(width, height, margin, up_color, down_color, grid_color, axis_color, label_color, color_by_open)` — Time-series chart renderer
- `TimeSeriesChartRenderer.render(data, period, title, date_key, value_key)` — Render chart with period filtering
- `normalize_timeseries_data(data, date_key, value_key)` — Normalize various input formats
- `extract_values(normalized_data)` — Extract values from normalized data
- `extract_dates(normalized_data)` — Extract dates from normalized data

REST API endpoints:
- `POST /sparkline-raw` — Render sparkline from JSON data
- `POST /chart-raw` — Render chart from JSON data
- `GET /test-charts` — Interactive test UI
- `GET /health` — Health check endpoint

Stable request models:
- `SparklineRequest` — Sparkline rendering parameters
- `ChartRequest` — Chart rendering parameters (period, title, dimensions, styling)

---

## Compatibility

- Python 3.9+
- Pure Python with zero external dependencies for core library
- FastAPI and Uvicorn for REST service (optional)
- Jinja2 for test UI (optional)

---

## Notes

This release establishes the 0.1.0 API contract for `timeseries-sparklines`.

The focus of this release is server-side SVG rendering for time-series data visualization in SSR applications, dashboards, and agentic systems. The library is designed as a pure rendering engine that accepts normalized time-series data and returns production-ready SVG markup.

Key design decisions:
- Data-agnostic: Does not fetch, store, or poll data
- Server-side rendering: No frontend chart libraries required
- Flexible input: Auto-normalizes 6+ JSONB formats
- Period-based filtering: Time windows for historical data
- Responsive SVG: CSS-scalable vector graphics

Backward compatibility will be maintained within the 0.1.x series.
