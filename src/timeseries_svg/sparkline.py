"""Sparkline SVG renderer."""

from typing import Any, List, Optional, Tuple
from timeseries_svg.data import extract_values, normalize_timeseries_data


class SparklineRenderer:
    """Render sparkline SVG charts from time series data."""
    
    def __init__(
        self,
        width: int = 96,
        height: int = 24,
        stroke_width: float = 1.8,
        baseline_color: str = "rgba(148,163,184,0.35)",
        up_color: str = "#12b76a",
        down_color: str = "#f04438",
        show_baseline: bool = True,
        color_by_open: bool = False,
    ):
        """
        Initialize sparkline renderer.
        
        Args:
            width: SVG width in pixels
            height: SVG height in pixels
            stroke_width: Line stroke width
            baseline_color: Color for baseline reference line
            up_color: Color for upward trend
            down_color: Color for downward trend
            show_baseline: Whether to show baseline reference line
            color_by_open: If True, color segments based on open price (first point)
        """
        self.width = width
        self.height = height
        self.stroke_width = stroke_width
        self.baseline_color = baseline_color
        self.up_color = up_color
        self.down_color = down_color
        self.show_baseline = show_baseline
        self.color_by_open = color_by_open
    
    def render(self, data: Any, **normalize_kwargs) -> str:
        """
        Render sparkline SVG from input data.
        
        Args:
            data: Input data in any supported format (list, dict, etc.)
            **normalize_kwargs: Arguments passed to normalize_timeseries_data
        
        Returns:
            SVG string
        """
        normalized = normalize_timeseries_data(data, **normalize_kwargs)
        values = extract_values(normalized)
        
        if len(values) < 2:
            return self._render_empty()
        
        return self._render_svg(values)
    
    def _render_empty(self) -> str:
        """Render empty sparkline placeholder."""
        return f'<svg width="100%" height="{self.height}" viewBox="0 0 {self.width} {self.height}" role="img" aria-hidden="true"></svg>'
    
    def _render_svg(self, values: List[float]) -> str:
        """Render sparkline SVG from numeric values."""
        # Filter to finite numbers
        numeric_values = [v for v in values if isinstance(v, (int, float))]
        
        if len(numeric_values) < 2:
            return self._render_empty()
        
        # Calculate scaling
        min_val = min(numeric_values)
        max_val = max(numeric_values)
        range_val = max_val - min_val
        denominator = max(1, len(numeric_values) - 1)
        
        # Calculate coordinates for all points
        coords = []
        for idx, value in enumerate(numeric_values):
            x = (idx / denominator) * self.width
            normalized = 0.5 if range_val == 0 else (value - min_val) / range_val
            y = (1 - normalized) * self.height
            coords.append((x, y))
        
        # Baseline Y position (at open price)
        open_price = numeric_values[0]
        open_normalized = 0.5 if range_val == 0 else (open_price - min_val) / range_val
        baseline_y = ((1 - open_normalized) * self.height)
        
        # Build SVG
        svg_parts = []
        
        if self.show_baseline:
            svg_parts.append(
                f'<line x1="0" y1="{baseline_y:.2f}" x2="{self.width}" y2="{baseline_y:.2f}" '
                f'stroke="{self.baseline_color}" stroke-width="1"></line>'
            )
        
        if self.color_by_open:
            # Render segments with different colors based on open price
            for idx in range(len(coords) - 1):
                x1, y1 = coords[idx]
                x2, y2 = coords[idx + 1]
                current_price = numeric_values[idx]
                color = self.up_color if current_price >= open_price else self.down_color
                svg_parts.append(
                    f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                    f'stroke="{color}" stroke-width="{self.stroke_width}" stroke-linecap="round"></line>'
                )
        else:
            # Single polyline with trend color
            points = [f"{x:.2f},{y:.2f}" for x, y in coords]
            trend_up = numeric_values[-1] >= numeric_values[0]
            stroke = self.up_color if trend_up else self.down_color
            svg_parts.append(
                f'<polyline fill="none" stroke="{stroke}" stroke-width="{self.stroke_width}" '
                f'stroke-linecap="round" stroke-linejoin="round" points="{" ".join(points)}"></polyline>'
            )
        
        return (
            f'<svg width="100%" height="{self.height}" viewBox="0 0 {self.width} {self.height}" '
            f'role="img" aria-hidden="true">{"".join(svg_parts)}</svg>'
        )
