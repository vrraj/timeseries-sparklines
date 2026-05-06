"""Time series chart SVG renderer."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from timeseries_svg.data import extract_values, extract_dates, normalize_timeseries_data


class TimeSeriesChartRenderer:
    """Render interactive time series chart SVGs."""
    
    PERIOD_LABEL_RULES = {
        '5D': {'interval': 1, 'format': {'weekday': 'short'}},
        '1M': {'interval': 7, 'format': {'month': 'short', 'day': 'numeric'}},
        '3M': {'interval': 21, 'format': {'month': 'short', 'day': 'numeric'}},
        '6M': {'interval': 30, 'format': {'month': 'short'}},
        '1Y': {'interval': 60, 'format': {'month': 'short'}},
    }
    
    def __init__(
        self,
        width: int = 760,
        height: int = 320,
        margin: Optional[Dict[str, int]] = None,
        up_color: str = "#16a34a",
        down_color: str = "#dc2626",
        grid_color: str = "rgba(148,163,184,0.35)",
        axis_color: str = "#94a3b8",
        label_color: str = "#64748b",
        tooltip_bg: str = "#ffffff",
        tooltip_border: str = "rgba(148,163,184,0.45)",
        color_by_open: bool = False,
    ):
        """
        Initialize chart renderer.
        
        Args:
            width: SVG width in pixels
            height: SVG height in pixels
            margin: Chart margins {top, right, bottom, left}
            up_color: Color for upward trend
            down_color: Color for downward trend
            grid_color: Grid line color
            axis_color: Axis line color
            label_color: Axis label color
            tooltip_bg: Tooltip background color
            tooltip_border: Tooltip border color
            color_by_open: If True, color segments based on open price (first point)
        """
        self.width = width
        self.height = height
        self.margin = margin or {'top': 16, 'right': 20, 'bottom': 44, 'left': 58}
        self.up_color = up_color
        self.down_color = down_color
        self.grid_color = grid_color
        self.axis_color = axis_color
        self.label_color = label_color
        self.tooltip_bg = tooltip_bg
        self.tooltip_border = tooltip_border
        self.color_by_open = color_by_open
        
        self.plot_width = width - self.margin['left'] - self.margin['right']
        self.plot_height = height - self.margin['top'] - self.margin['bottom']
    
    def _slice_data_by_period(self, values: List[float], dates: List[str], period) -> tuple:
        """
        Slice data based on period using time-based windows.
        
        Args:
            values: List of values
            dates: List of dates
            period: Time period (5D, 1M, 3M, 6M, 1Y) or custom timedelta object
        
        Returns:
            Tuple of sliced (values, dates)
        """
        from datetime import timedelta, datetime
        
        # Predefined period deltas
        period_deltas = {
            '5D': timedelta(days=5),
            '1W': timedelta(weeks=1),
            '2W': timedelta(weeks=2),
            '1M': timedelta(days=30),
            '3M': timedelta(days=90),
            '6M': timedelta(days=180),
            '1Y': timedelta(days=365),
        }
        
        # Handle custom timedelta or predefined period string
        if isinstance(period, timedelta):
            delta = period
        else:
            delta = period_deltas.get(period)
        
        if delta is None:
            return values, dates
        
        if len(dates) == 0:
            return values, dates
        
        # Parse the most recent date
        try:
            if 'T' in dates[-1]:
                latest_date = datetime.fromisoformat(dates[-1].replace('Z', '+00:00'))
            else:
                parts = dates[-1].split('-')
                latest_date = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
        except (ValueError, TypeError, IndexError):
            return values, dates
        
        # Calculate cutoff date
        cutoff_date = latest_date - delta
        
        # Filter data points within the time window
        filtered_values = []
        filtered_dates = []
        
        for date_str, value in zip(dates, values):
            try:
                if 'T' in date_str:
                    current_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                else:
                    parts = date_str.split('-')
                    current_date = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
                
                if current_date >= cutoff_date:
                    filtered_dates.append(date_str)
                    filtered_values.append(value)
            except (ValueError, TypeError, IndexError):
                # Skip invalid dates
                continue
        
        return filtered_values, filtered_dates
    
    def render(
        self,
        data: Any,
        period: str = "1M",
        title: Optional[str] = None,
        **normalize_kwargs
    ) -> str:
        """
        Render time series chart SVG.
        
        Args:
            data: Input data in any supported format
            period: Time period for label formatting (5D, 1M, 3M, 6M, 1Y)
            title: Optional chart title
            **normalize_kwargs: Arguments passed to normalize_timeseries_data
        
        Returns:
            SVG string
        """
        normalized = normalize_timeseries_data(data, **normalize_kwargs)
        values = extract_values(normalized)
        dates = extract_dates(normalized)
        
        # Slice data based on period
        values, dates = self._slice_data_by_period(values, dates, period)
        
        if len(values) < 2 or len(dates) < 2:
            return self._render_empty("Not enough data for chart")
        
        return self._render_svg(values, dates, period, title)
    
    def _render_empty(self, message: str = "No data available") -> str:
        """Render empty chart placeholder."""
        return f'<div class="empty-state">{message}</div>'
    
    def _render_svg(
        self,
        values: List[float],
        dates: List[str],
        period,
        title: Optional[str]
    ) -> str:
        """Render chart SVG from values and dates."""
        # Calculate scaling
        min_val = min(values)
        max_val = max(values)
        range_val = max(0.000001, max_val - min_val)
        denominator = max(1, len(values) - 1)
        
        # Coordinate functions
        def x_for_index(idx: int) -> float:
            return self.margin['left'] + (idx / denominator) * self.plot_width
        
        def y_for_price(price: float) -> float:
            normalized = (price - min_val) / range_val
            return self.margin['top'] + (1 - normalized) * self.plot_height
        
        # Generate polyline points
        points = []
        for idx, price in enumerate(values):
            x = x_for_index(idx)
            y = y_for_price(price)
            points.append(f"{x:.2f},{y:.2f}")
        
        # Trend color
        trend_up = values[-1] >= values[0]
        stroke = self.up_color if trend_up else self.down_color
        
        # Y-axis ticks
        y_tick_count = 5
        y_ticks = []
        for idx in range(y_tick_count):
            ratio = idx / (y_tick_count - 1)
            value = max_val - (range_val * ratio)
            y = self.margin['top'] + (self.plot_height * ratio)
            y_ticks.append({'value': value, 'y': y})
        
        # X-axis ticks based on period
        from datetime import timedelta
        # Use default label rule for custom timedelta periods
        if isinstance(period, timedelta):
            label_rule = self.PERIOD_LABEL_RULES['1M']
        else:
            label_rule = self.PERIOD_LABEL_RULES.get(period, self.PERIOD_LABEL_RULES['1M'])
        x_ticks = []
        interval = max(1, int(label_rule['interval']))
        for idx in range(0, len(dates), interval):
            x_ticks.append({
                'index': idx,
                'x': x_for_index(idx),
                'label': self._format_date(dates[idx], label_rule['format'])
            })
        # Ensure last point is included
        if not any(t['index'] == len(dates) - 1 for t in x_ticks):
            x_ticks.append({
                'index': len(dates) - 1,
                'x': x_for_index(len(dates) - 1),
                'label': self._format_date(dates[-1], label_rule['format'])
            })
        
        # Initial hover state (last point)
        initial_idx = len(values) - 1
        initial_x = x_for_index(initial_idx)
        initial_y = y_for_price(values[initial_idx])
        
        # Tooltip positioning
        tooltip_width = 184
        tooltip_height = 34
        tooltip_x = min(self.width - tooltip_width - 8, max(8, initial_x - tooltip_width - 8))
        tooltip_y = max(8, self.margin['top'])
        
        # Build SVG
        svg_parts = []
        
        # Y-axis grid lines and labels
        for tick in y_ticks:
            svg_parts.append(
                f'<line x1="{self.margin["left"]}" y1="{tick["y"]:.2f}" '
                f'x2="{self.width - self.margin["right"]:.2f}" y2="{tick["y"]:.2f}" '
                f'stroke="{self.grid_color}" stroke-width="1"></line>'
            )
            svg_parts.append(
                f'<text x="{self.margin["left"] - 8:.2f}" y="{tick["y"] + 4:.2f}" '
                f'text-anchor="end" fill="{self.label_color}" font-size="11">'
                f'{self._format_value(tick["value"])}</text>'
            )
        
        # X-axis labels
        for tick in x_ticks:
            svg_parts.append(
                f'<text x="{tick["x"]:.2f}" y="{self.height - 12:.2f}" '
                f'text-anchor="middle" fill="{self.label_color}" font-size="11">'
                f'{tick["label"]}</text>'
            )
        
        # Axis lines
        svg_parts.append(
            f'<line x1="{self.margin["left"]}" y1="{self.height - self.margin["bottom"]:.2f}" '
            f'x2="{self.width - self.margin["right"]:.2f}" y2="{self.height - self.margin["bottom"]:.2f}" '
            f'stroke="{self.axis_color}" stroke-width="1.25"></line>'
        )
        svg_parts.append(
            f'<line x1="{self.margin["left"]}" y1="{self.margin["top"]}" '
            f'x2="{self.margin["left"]}" y2="{self.height - self.margin["bottom"]:.2f}" '
            f'stroke="{self.axis_color}" stroke-width="1.25"></line>'
        )
        
        # Data line
        if self.color_by_open:
            # Render segments with different colors based on open price
            open_price = values[0]
            for idx in range(len(points) - 1):
                current_price = values[idx]
                color = self.up_color if current_price >= open_price else self.down_color
                svg_parts.append(
                    f'<line x1="{points[idx].split(",")[0]}" y1="{points[idx].split(",")[1]}" '
                    f'x2="{points[idx + 1].split(",")[0]}" y2="{points[idx + 1].split(",")[1]}" '
                    f'stroke="{color}" stroke-width="2.25" stroke-linecap="round"></line>'
                )
        else:
            # Single polyline with trend color
            svg_parts.append(
                f'<polyline fill="none" stroke="{stroke}" stroke-width="2.25" '
                f'stroke-linecap="round" stroke-linejoin="round" points="{" ".join(points)}"></polyline>'
            )
        
        # Title if provided
        if title:
            svg_parts.insert(0, f'<text x="{self.width / 2:.2f}" y="27" text-anchor="middle" fill="#0f172a" font-size="14" font-weight="600">{title}</text>')
        
        return (
            f'<svg width="100%" height="{self.height}" viewBox="0 0 {self.width} {self.height}" '
            f'role="img" aria-hidden="true">{"".join(svg_parts)}</svg>'
        )
    
    def _format_date(self, date_str: str, format_options: Dict[str, str]) -> str:
        """Format date string according to options."""
        try:
            # Try parsing ISO format
            if 'T' in date_str:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                # Try YYYY-MM-DD
                parts = date_str.split('-')
                if len(parts) == 3:
                    dt = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
                else:
                    return date_str
            return dt.strftime(self._strftime_from_options(format_options))
        except (ValueError, TypeError):
            return date_str
    
    def _strftime_from_options(self, format_options: Dict[str, str]) -> str:
        """Convert Intl-style format options to strftime format."""
        mapping = {
            'weekday:short': '%a',
            'month:short': '%b',
            'day:numeric': '%d',
            'year:numeric': '%Y',
        }
        key = ','.join(f"{k}:{v}" for k, v in format_options.items())
        return mapping.get(key, '%b %d')
    
    def _format_value(self, value: float) -> str:
        """Format numeric value as currency/number."""
        return f"${value:.2f}"
