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
    uvicorn.run("timeseries_svg.api:create_app", host="0.0.0.0", port=9300, factory=True)
