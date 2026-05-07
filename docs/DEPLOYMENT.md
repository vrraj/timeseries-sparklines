---
layout: default
title: "Deployment Guide | Timeseries SVG"
description: "Installation and deployment instructions for timeseries-sparklines package."
---

# Deployment Guide

This guide explains how to deploy the timeseries-sparklines package on other machines.

## Package Files

After building, the following distribution files are created in the `dist/` directory:
- `timeseries_svg-0.1.0-py3-none-any.whl` (wheel file, recommended for installation)
- `timeseries_svg-0.1.0.tar.gz` (source distribution)

## Installation on Target Machine

### Option 1: Install from Wheel File (Recommended)

1. **Transfer the wheel file** to the target machine:
   ```bash
   # From your local machine
   scp dist/timeseries_svg-0.1.0-py3-none-any.whl user@target-machine:/path/to/deploy/
   ```

2. **Install the package** on the target machine:
   ```bash
   pip install timeseries_svg-0.1.0-py3-none-any.whl
   ```

### Option 2: Install from Source Distribution

1. **Transfer the tar.gz file** to the target machine:
   ```bash
   scp dist/timeseries_svg-0.1.0.tar.gz user@target-machine:/path/to/deploy/
   ```

2. **Install the package** on the target machine:
   ```bash
   pip install timeseries_svg-0.1.0.tar.gz
   ```

### Option 3: Install from Git Repository (if available)

If you have a git repository:
```bash
pip install git+https://github.com/vrraj/timeseries-sparklines.git
```

## Installation with API Dependencies

If you want to use the FastAPI server, install with API dependencies:
```bash
pip install timeseries_svg-0.1.0-py3-none-any.whl[api]
```

## Running the API Server

After installation, you can run the API server using the provided CLI command:
```bash
timeseries-server
```

This will start a FastAPI server on `http://0.0.0.0:9300`

### API Endpoints

- `POST /sparkline-raw` - Render sparkline from JSON data
- `POST /chart-raw` - Render chart from JSON data
- `GET /health` - Health check endpoint

## Using as a Library

### Basic Library Usage

```python
from timeseries_svg import SparklineRenderer, TimeSeriesChartRenderer

# Sparkline example
data = [
    {"d": "2024-01-01", "c": 100.0},
    {"d": "2024-01-02", "c": 102.5},
    {"d": "2024-01-03", "c": 101.2},
]

renderer = SparklineRenderer(width=96, height=32)
svg = renderer.render(data)
print(svg)
```

### Integration with Your Application

```python
from fastapi import FastAPI, Response
from timeseries_svg import SparklineRenderer

app = FastAPI()
renderer = SparklineRenderer()

@app.post("/api/sparkline")
async def get_sparkline(request: dict):
    # Your data fetching logic here
    data = fetch_your_data(request)
    
    # Render SVG
    svg = renderer.render(data, color_by_open=True)
    
    return Response(content=svg, media_type="image/svg+xml")
```

## System Requirements

- Python 3.9 or higher
- pip package manager

### For API Server:
- FastAPI (install with `[api]` extra)
- Uvicorn (install with `[api]` extra)

## Verification

After installation, verify the package is working:

```python
python -c "from timeseries_svg import SparklineRenderer; print('Installation successful')"
```

Or test the API server:
```bash
timeseries-server
# Then in another terminal:
curl http://localhost:9300/health
```

## Rebuilding the Package

If you make changes to the source code, rebuild the package:

```bash
# Clean previous builds
rm -rf dist/ build/ src/*.egg-info

# Build new package
python -m build
```

## Troubleshooting

### Import Errors
If you get import errors, ensure you're using the correct Python environment where the package was installed.

### API Server Won't Start
Make sure you installed with API dependencies:
```bash
pip install timeseries_svg-0.1.0-py3-none-any.whl[api]
```

### Permission Errors
Use a virtual environment to avoid permission issues:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install timeseries_svg-0.1.0-py3-none-any.whl
```

## Production Deployment

For production deployment, consider:

1. **Use a process manager** (systemd, supervisor) to keep the API server running
2. **Use a reverse proxy** (nginx) in front of the API server
3. **Configure proper logging** and monitoring
4. **Use environment variables** for configuration

### Example systemd Service

Create `/etc/systemd/system/timeseries-server.service`:
```ini
[Unit]
Description=Timeseries SVG API Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/timeseries-server
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable timeseries-server
sudo systemctl start timeseries-server
```

## License

MIT License - see LICENSE file for details.
