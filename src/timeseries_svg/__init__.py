"""timeseries-svg: General-purpose time series SVG plotting library."""

from timeseries_svg.sparkline import SparklineRenderer
from timeseries_svg.chart import TimeSeriesChartRenderer
from timeseries_svg.bar_chart import BarChartRenderer
from timeseries_svg.data import normalize_timeseries_data, extract_values, extract_dates

__version__ = "0.1.0"
__all__ = [
    "SparklineRenderer",
    "TimeSeriesChartRenderer",
    "BarChartRenderer",
    "normalize_timeseries_data",
    "extract_values",
    "extract_dates",
]
