"""Pydantic models for Timeseries SVG API."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SparklineRequest(BaseModel):
    """Request model for sparkline rendering."""
    
    data: Any = Field(..., description="Time series data in any supported format")
    width: int = Field(96, description="SVG width in pixels")
    height: int = Field(24, description="SVG height in pixels")
    stroke_width: float = Field(1.8, description="Line stroke width")
    baseline_color: str = Field("rgba(148,163,184,0.35)", description="Baseline color")
    up_color: str = Field("#12b76a", description="Upward trend color")
    down_color: str = Field("#f04438", description="Downward trend color")
    show_baseline: bool = Field(True, description="Show baseline reference line")
    color_by_open: bool = Field(False, description="Color segments based on open price (first point)")
    date_key: Optional[str] = Field(None, description="Custom date key for dict format")
    value_key: Optional[str] = Field(None, description="Custom value key for dict format")


class ChartRequest(BaseModel):
    """Request model for chart rendering."""
    
    data: Any = Field(..., description="Time series data in any supported format")
    period: str = Field("1M", description="Time period for label formatting (5D, 1M, 3M, 6M, 1Y)")
    title: Optional[str] = Field(None, description="Chart title")
    width: int = Field(760, description="SVG width in pixels")
    height: int = Field(320, description="SVG height in pixels")
    margin: Optional[Dict[str, int]] = Field(None, description="Chart margins")
    up_color: str = Field("#16a34a", description="Upward trend color")
    down_color: str = Field("#dc2626", description="Downward trend color")
    grid_color: str = Field("rgba(148,163,184,0.35)", description="Grid line color")
    axis_color: str = Field("#94a3b8", description="Axis line color")
    label_color: str = Field("#64748b", description="Axis label color")
    color_by_open: bool = Field(False, description="Color segments based on open price (first point)")
    date_key: Optional[str] = Field(None, description="Custom date key for dict format")
    value_key: Optional[str] = Field(None, description="Custom value key for dict format")


class SVGResponse(BaseModel):
    """Response model for SVG rendering."""
    
    success: bool = Field(..., description="Whether rendering was successful")
    svg: Optional[str] = Field(None, description="SVG string")
    message: Optional[str] = Field(None, description="Error or status message")


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Package version")
