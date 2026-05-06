"""API components for Timeseries SVG."""

import uvicorn

from .models import (
    SparklineRequest,
    ChartRequest,
    SVGResponse,
    HealthResponse,
)
from .routes import create_app

__all__ = [
    "SparklineRequest",
    "ChartRequest",
    "SVGResponse",
    "HealthResponse",
    "create_app",
]


def main():
    """CLI entry point for running the API server."""
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=9300)
