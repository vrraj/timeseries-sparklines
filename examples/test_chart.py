#!/usr/bin/env python3
"""
Test script for timeseries-sparklines library.
Tests sparkline, bar chart, and line chart rendering.
"""

# Test sparkline
from timeseries_svg import SparklineRenderer

print("=" * 60)
print("SPARKLINE TEST")
print("=" * 60)

renderer = SparklineRenderer(width=96, height=32)
svg = renderer.render([100, 102.5, 101.2, 105, 103.8])
print(svg)
print()

# Test bar chart
from timeseries_svg import BarChartRenderer

print("=" * 60)
print("BAR CHART TEST")
print("=" * 60)

data = [
    {"d": "2024-01-01", "v": 100.0},
    {"d": "2024-02-01", "v": 102.5},
    {"d": "2024-03-01", "v": 101.2},
    {"d": "2024-04-01", "v": 105.0},
    {"d": "2024-05-01", "v": 103.8},
]

renderer = BarChartRenderer(y_axis_label="Value", y_axis_offset=0.1)
svg = renderer.render(data, period="6M", title="Monthly Values")
print(svg)
print()

# Test line chart
from timeseries_svg import TimeSeriesChartRenderer

print("=" * 60)
print("LINE CHART TEST")
print("=" * 60)

renderer = TimeSeriesChartRenderer(y_axis_label="Value", y_axis_offset=0.1)
svg = renderer.render(data, period="6M", title="Value Trend")
print(svg)
print()

print("=" * 60)
print("All tests completed successfully")
print("=" * 60)
