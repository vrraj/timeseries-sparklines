"""FastAPI routes for Timeseries SVG API."""

import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response

from ..sparkline import SparklineRenderer
from ..chart import TimeSeriesChartRenderer
from ..bar_chart import BarChartRenderer
from .. import __version__
from .models import (
    SparklineRequest,
    ChartRequest,
    SVGResponse,
    HealthResponse,
)


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title="Timeseries SVG",
        description="General-purpose time series SVG plotting API",
        version=__version__,
    )
    
    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Serve the API landing page."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Timeseries SVG API</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
                h1 {{ color: #0f172a; }}
                .endpoint {{ background: #f1f5f9; padding: 16px; border-radius: 8px; margin: 16px 0; }}
                .method {{ color: #059669; font-weight: bold; }}
                .path {{ color: #0ea5e9; font-family: monospace; }}
                code {{ background: #e2e8f0; padding: 2px 6px; border-radius: 4px; }}
                svg {{ display: block; margin: 16px 0; }}
            </style>
        </head>
        <body>
            <h1>Timeseries SVG API</h1>
            <p>General-purpose time series SVG plotting service</p>
            <p>Version: {__version__}</p>
            
            <h2>Endpoints</h2>
            
            <div class="endpoint">
                <span class="method">POST</span> <span class="path">/sparkline</span>
                <p>Render a sparkline SVG from time series data</p>
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> <span class="path">/chart</span>
                <p>Render a full time series chart SVG</p>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="path">/health</span>
                <p>Health check endpoint</p>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="path">/docs</span>
                <p>Interactive API documentation (Swagger UI)</p>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="path">/test-charts</span>
                <p>Visual test page with rendered examples</p>
            </div>
            
            <h2>Example Usage</h2>
            <pre><code>curl -X POST http://localhost:9300/sparkline \\
  -H "Content-Type: application/json" \\
  -d '{{"data": [100.0, 102.5, 101.2, 105.0]}}'</code></pre>
        </body>
        </html>
        """
    
    @app.get("/test-charts", response_class=HTMLResponse)
    async def test_page():
        """Serve a visual test page."""
        from ..sparkline import SparklineRenderer
        from ..chart import TimeSeriesChartRenderer
        
        # Generate examples
        sparkline_data = [100.0, 102.5, 101.2, 105.0, 103.8, 107.0, 103, 100, 90, 95, 99, 105, 106, 100, 110, 105, 95, 117, 118, 120, 128, 130, 120, 117, 118, 116, 125, 130, 134]
        sparkline_renderer = SparklineRenderer(width=200, height=64)
        sparkline_svg = sparkline_renderer.render(sparkline_data)
        
        # Chart data with dates for period filtering
        chart_data_with_dates = [
            {"d": "2024-01-01", "c": 100.0},
            {"d": "2024-01-02", "c": 102.5},
            {"d": "2024-01-03", "c": 101.2},
            {"d": "2024-01-04", "c": 105.0},
            {"d": "2024-01-05", "c": 103.8},
            {"d": "2024-01-08", "c": 107.0},
            {"d": "2024-01-09", "c": 103.0},
            {"d": "2024-01-10", "c": 100.0},
            {"d": "2024-01-11", "c": 90.0},
            {"d": "2024-01-12", "c": 95.0},
            {"d": "2024-01-15", "c": 99.0},
            {"d": "2024-01-16", "c": 105.0},
            {"d": "2024-01-17", "c": 106.0},
            {"d": "2024-01-18", "c": 100.0},
            {"d": "2024-01-19", "c": 110.0},
            {"d": "2024-01-22", "c": 105.0},
            {"d": "2024-01-23", "c": 95.0},
            {"d": "2024-01-24", "c": 117.0},
            {"d": "2024-01-25", "c": 118.0},
            {"d": "2024-01-26", "c": 120.0},
            {"d": "2024-01-29", "c": 128.0},
            {"d": "2024-01-30", "c": 130.0},
            {"d": "2024-01-31", "c": 120.0},
            {"d": "2024-02-01", "c": 117.0},
            {"d": "2024-02-02", "c": 118.0},
            {"d": "2024-02-05", "c": 116.0},
            {"d": "2024-02-06", "c": 125.0},
            {"d": "2024-02-07", "c": 130.0},
            {"d": "2024-02-08", "c": 134.0},
        ]
        chart_renderer = TimeSeriesChartRenderer()
        chart_svg = chart_renderer.render(chart_data_with_dates, period="5D", title="Sample Chart")
        
        sparkline_json = json.dumps(chart_data_with_dates, indent=2)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Timeseries SVG - Visual Test</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }}
                h1 {{ color: #0f172a; }}
                h2 {{ color: #334155; margin-top: 32px; }}
                .card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px; margin: 16px 0; }}
                .grid-two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
                @media (max-width: 768px) {{ .grid-two {{ grid-template-columns: 1fr; }} }}
                svg {{ display: block; margin: 16px 0; }}
                .back {{ color: #3b82f6; text-decoration: none; }}
                .back:hover {{ text-decoration: underline; }}
                textarea {{ width: 100%; min-height: 120px; font-family: monospace; padding: 12px; border: 1px solid #cbd5e1; border-radius: 6px; margin: 8px 0; }}
                label {{ display: block; margin: 8px 0 4px; font-weight: 500; }}
                select, input {{ padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px; margin: 8px 0; }}
                button {{ background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: 500; }}
                button:hover {{ background: #2563eb; }}
                .format-pill {{ background: #e2e8f0; color: #475569; border: 1px solid #cbd5e1; padding: 6px 12px; border-radius: 16px; cursor: pointer; font-size: 13px; font-weight: 500; margin-right: 6px; margin-bottom: 6px; }}
                .format-pill:hover {{ background: #cbd5e1; }}
                .result {{ margin-top: 16px; }}
                #result-container {{ margin-top: 24px; padding: 20px; background: #f1f5f9; border-radius: 8px; border: 1px solid #e2e8f0; min-height: 100px; }}
            </style>
        </head>
        <body>
            <a href="/" class="back">← Back to API</a>
            <a href="/usage-guide" class="back" style="margin-left: 20px;" target="_blank">Usage Guide</a>
            <h1>Sparklines and Interactive Chart Testing</h1>
            
            <div class="card">
                <label>Chart Type:</label>
                <select id="chartType">
                    <option value="sparkline">Sparkline</option>
                    <option value="chart">Line Chart</option>
                    <option value="bar">Bar Chart</option>
                </select>
                
                <label for="dataInput">Data (JSON):</label>
                <div style="margin-bottom: 8px; display: flex; align-items: center;">
                    <label style="font-size: 13px; color: #64748b; margin-right: 8px; margin-bottom: 0;">Supported Formats:</label>
                    <button type="button" class="format-pill" onclick="loadFormat('list_values')">List of values</button>
                    <button type="button" class="format-pill" onclick="loadFormat('dict_date_value')">Dict with date/value</button>
                </div>
                <textarea id="dataInput" placeholder='Enter JSON data, e.g.: [100.0, 102.5, 101.2] or [{{"d": "2024-01-01", "c": 150.0}}, ...]'>{sparkline_json}</textarea>
                
                <label>
                    <input type="checkbox" id="colorByOpen"> Color segments by open price (green = above open, red = below open)
                </label>
                
                <div id="chartOptions" style="display: none;">
                    <div style="display: flex; gap: 16px; margin-bottom: 8px;">
                        <div style="flex: 1;">
                            <label for="period">Period:</label>
                            <select id="period">
                                <option value="5D">5D (5 days)</option>
                                <option value="1W">1W (1 week)</option>
                                <option value="2W">2W (2 weeks)</option>
                                <option value="1M">1M (30 days)</option>
                                <option value="3M">3M (90 days)</option>
                                <option value="6M">6M (180 days)</option>
                                <option value="1Y">1Y (365 days)</option>
                                <option value="custom">Custom (specify below)</option>
                            </select>
                        </div>
                        <div style="flex: 1;">
                            <label for="title">Title (optional):</label>
                            <input type="text" id="title" placeholder="Chart Title" style="width: 100%;">
                        </div>
                    </div>
                    
                    <div id="customPeriod" style="display: none;">
                        <label for="customDays">Custom Period (days):</label>
                        <input type="number" id="customDays" placeholder="Enter number of days" min="1">
                    </div>
                </div>
                
                <button onclick="renderChart()">Render</button>
                
                <div id="result-container"></div>
            </div>
            
            <script>
                const chartTypeSelect = document.getElementById('chartType');
                const chartOptions = document.getElementById('chartOptions');
                const periodSelect = document.getElementById('period');
                const customPeriodDiv = document.getElementById('customPeriod');
                
                // Example data formats
                const formatExamples = {{
                    'list_values': [100, 102.5, 101.2, 105, 119, 103.8, 107, 103, 100, 90, 95, 99, 105, 106, 100, 110, 120, 125, 114, 122, 130],
                    'dict_date_value': [
                        {{"d": "2024-01-01", "v": 100.0}},
                        {{"d": "2024-01-02", "v": 102.5}},
                        {{"d": "2024-01-03", "v": 101.2}},
                        {{"d": "2024-01-04", "v": 105.0}},
                        {{"d": "2024-01-05", "v": 103.8}},
                        {{"d": "2024-01-08", "v": 107.0}},
                        {{"d": "2024-01-09", "v": 103.0}},
                        {{"d": "2024-01-10", "v": 100.0}},
                        {{"d": "2024-01-11", "v": 90.0}},
                        {{"d": "2024-01-12", "v": 95.0}},
                        {{"d": "2024-01-15", "v": 99.0}},
                        {{"d": "2024-01-16", "v": 105.0}},
                        {{"d": "2024-01-17", "v": 106.0}},
                        {{"d": "2024-01-18", "v": 100.0}},
                        {{"d": "2024-01-19", "v": 110.0}}
                    ]
                }};
                
                function loadFormat(format) {{
                    const dataInput = document.getElementById('dataInput');
                    dataInput.value = JSON.stringify(formatExamples[format], null, 2);
                }}
                
                chartTypeSelect.addEventListener('change', function() {{
                    chartOptions.style.display = (this.value === 'chart' || this.value === 'bar') ? 'block' : 'none';
                }});
                
                periodSelect.addEventListener('change', function() {{
                    customPeriodDiv.style.display = this.value === 'custom' ? 'block' : 'none';
                }});
                
                async function renderChart() {{
                    const chartType = document.getElementById('chartType').value;
                    const dataInput = document.getElementById('dataInput').value;
                    const resultContainer = document.getElementById('result-container');
                    const colorByOpen = document.getElementById('colorByOpen').checked;

                    let endpoint = chartType === 'sparkline' ? '/sparkline-raw' : '/chart-raw';
                    let body = {{ data: JSON.parse(dataInput) }};

                    if (chartType === 'sparkline' || chartType === 'chart' || chartType === 'bar') {{
                        body.color_by_open = colorByOpen;
                    }}

                    if (chartType === 'chart' || chartType === 'bar') {{
                        body.chart_type = chartType;
                        const periodValue = document.getElementById('period').value;
                        if (periodValue === 'custom') {{
                            const customDays = parseInt(document.getElementById('customDays').value);
                            if (customDays && customDays > 0) {{
                                body.period_days = customDays;
                            }} else {{
                                body.period = '1M'; // fallback
                            }}
                        }} else {{
                            body.period = periodValue;
                        }}
                        const title = document.getElementById('title').value;
                        if (title) body.title = title;
                    }}
                    
                    try {{
                        resultContainer.innerHTML = '<p>Loading...</p>';
                        const response = await fetch(endpoint, {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify(body)
                        }});
                        
                        if (response.ok) {{
                            const svg = await response.text();
                            resultContainer.innerHTML = '<h3>Result:</h3>' + svg;
                        }} else {{
                            const error = await response.text();
                            resultContainer.innerHTML = '<p style="color: red;">Error: ' + error + '</p>';
                        }}
                    }} catch (e) {{
                        resultContainer.innerHTML = '<p style="color: red;">Error: ' + e.message + '</p>';
                    }}
                }}
            </script>
        </body>
        </html>
        """
        return html
    
    @app.get("/usage-guide", response_class=HTMLResponse)
    async def usage_guide():
        """Serve the usage guide markdown."""
        import os
        guide_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "docs", "usage-guide.md")
        try:
            with open(guide_path, 'r') as f:
                content = f.read()
                # Simple markdown to HTML conversion for basic formatting
                html = content.replace('```json', '<pre><code>').replace('```python', '<pre><code>').replace('```', '</code></pre>')
                html = html.replace('##', '<h2>').replace('#', '<h1>')
                html = html.replace('[← Back to Interactive Test](/test-charts)', '<a href="/test-charts" class="back">← Back to Interactive Test</a>')
                return f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Timeseries SVG - Data Formats</title>
                    <style>
                        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
                        h1 {{ color: #0f172a; }}
                        h2 {{ color: #334155; margin-top: 32px; }}
                        pre {{ background: #f1f5f9; padding: 16px; border-radius: 8px; overflow-x: auto; }}
                        code {{ background: #e2e8f0; padding: 2px 6px; border-radius: 4px; }}
                        .back {{ color: #3b82f6; text-decoration: none; }}
                        .back:hover {{ text-decoration: underline; }}
                    </style>
                </head>
                <body>{html}</body>
                </html>
                """
        except FileNotFoundError:
            return "<h1>Usage Guide Not Found</h1><p>docs/usage-guide.md not found</p>"
    
    @app.get("/health", response_model=HealthResponse)
    async def health():
        """Health check endpoint."""
        return HealthResponse(status="healthy", version=__version__)
    
    @app.post("/sparkline", response_model=SVGResponse)
    async def render_sparkline(request: SparklineRequest):
        """Render a sparkline SVG from time series data."""
        try:
            normalize_kwargs = {}
            if request.date_key:
                normalize_kwargs["date_key"] = request.date_key
            if request.value_key:
                normalize_kwargs["value_key"] = request.value_key
            
            renderer = SparklineRenderer(
                width=request.width,
                height=request.height,
                stroke_width=request.stroke_width,
                baseline_color=request.baseline_color,
                up_color=request.up_color,
                down_color=request.down_color,
                show_baseline=request.show_baseline,
                color_by_open=request.color_by_open,
            )
            
            svg = renderer.render(request.data, **normalize_kwargs)
            
            return SVGResponse(success=True, svg=svg)
            
        except Exception as e:
            return SVGResponse(success=False, message=str(e))
    
    @app.post("/chart", response_model=SVGResponse)
    async def render_chart(request: ChartRequest):
        """Render a full time series chart SVG."""
        try:
            normalize_kwargs = {}
            if request.date_key:
                normalize_kwargs["date_key"] = request.date_key
            if request.value_key:
                normalize_kwargs["value_key"] = request.value_key
            
            renderer = TimeSeriesChartRenderer(
                width=request.width,
                height=request.height,
                margin=request.margin,
                up_color=request.up_color,
                down_color=request.down_color,
                grid_color=request.grid_color,
                axis_color=request.axis_color,
                label_color=request.label_color,
                color_by_open=request.color_by_open,
            )
            
            svg = renderer.render(request.data, period=request.period, title=request.title, **normalize_kwargs)
            
            return SVGResponse(success=True, svg=svg)
            
        except Exception as e:
            return SVGResponse(success=False, message=str(e))
    
    @app.post("/sparkline-raw")
    async def render_sparkline_raw(request: SparklineRequest):
        """Render sparkline and return raw SVG (for direct embedding)."""
        try:
            normalize_kwargs = {}
            if request.date_key:
                normalize_kwargs["date_key"] = request.date_key
            if request.value_key:
                normalize_kwargs["value_key"] = request.value_key
            
            renderer = SparklineRenderer(
                width=request.width,
                height=request.height,
                stroke_width=request.stroke_width,
                baseline_color=request.baseline_color,
                up_color=request.up_color,
                down_color=request.down_color,
                show_baseline=request.show_baseline,
                color_by_open=request.color_by_open,
            )
            
            svg = renderer.render(request.data, **normalize_kwargs)
            
            return Response(content=svg, media_type="image/svg+xml")
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @app.post("/chart-raw")
    async def render_chart_raw(request: ChartRequest):
        """Render chart and return raw SVG (for direct embedding)."""
        try:
            from datetime import timedelta

            normalize_kwargs = {}
            if request.date_key:
                normalize_kwargs["date_key"] = request.date_key
            if request.value_key:
                normalize_kwargs["value_key"] = request.value_key

            # Route to appropriate renderer based on chart_type
            if request.chart_type == "bar":
                renderer = BarChartRenderer(
                    width=request.width,
                    height=request.height,
                    margin=request.margin,
                    bar_color=request.bar_color or "#3b82f6",
                    bar_width_ratio=request.bar_width_ratio or 0.7,
                    grid_color=request.grid_color,
                    axis_color=request.axis_color,
                    label_color=request.label_color,
                    color_by_open=request.color_by_open,
                    up_color=request.up_color,
                    down_color=request.down_color,
                )
            else:  # default to line chart
                renderer = TimeSeriesChartRenderer(
                    width=request.width,
                    height=request.height,
                    margin=request.margin,
                    up_color=request.up_color,
                    down_color=request.down_color,
                    grid_color=request.grid_color,
                    axis_color=request.axis_color,
                    label_color=request.label_color,
                    color_by_open=request.color_by_open,
                )

            # Handle custom period_days
            period = request.period
            if request.period_days:
                period = timedelta(days=request.period_days)

            svg = renderer.render(request.data, period=period, title=request.title, **normalize_kwargs)

            return Response(content=svg, media_type="image/svg+xml")

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler."""
        raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {str(exc)}")
    
    return app
