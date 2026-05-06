"""Example usage of timeseries-svg library."""

from timeseries_svg import SparklineRenderer, TimeSeriesChartRenderer, normalize_timeseries_data


def example_sparkline():
    """Example: Render a sparkline from various data formats."""
    
    print("=" * 60)
    print("SPARKLINE EXAMPLES")
    print("=" * 60)
    
    # Format 1: List of dicts (standard)
    data1 = [
        {"d": "2024-01-01", "c": 100.0},
        {"d": "2024-01-02", "c": 102.5},
        {"d": "2024-01-03", "c": 101.2},
        {"d": "2024-01-04", "c": 105.0},
        {"d": "2024-01-05", "c": 103.8},
    ]
    
    renderer = SparklineRenderer(width=96, height=24)
    svg1 = renderer.render(data1)
    print("\nFormat 1 (list of dicts):")
    print(svg1[:200] + "...")
    
    # Format 2: List of lists
    data2 = [
        ["2024-01-01", 100.0],
        ["2024-01-02", 102.5],
        ["2024-01-03", 101.2],
        ["2024-01-04", 105.0],
    ]
    
    svg2 = renderer.render(data2)
    print("\nFormat 2 (list of lists):")
    print(svg2[:200] + "...")
    
    # Format 3: Dict with date keys
    data3 = {
        "2024-01-01": 100.0,
        "2024-01-02": 102.5,
        "2024-01-03": 101.2,
        "2024-01-04": 105.0,
    }
    
    svg3 = renderer.render(data3)
    print("\nFormat 3 (dict with date keys):")
    print(svg3[:200] + "...")
    
    # Format 4: Simple value list
    data4 = [100.0, 102.5, 101.2, 105.0, 103.8, 107.0]
    svg4 = renderer.render(data4)
    print("\nFormat 4 (simple value list):")
    print(svg4[:200] + "...")


def example_chart():
    """Example: Render a full time series chart."""
    
    print("\n" + "=" * 60)
    print("CHART EXAMPLES")
    print("=" * 60)
    
    # Historical price data
    data = [
        {"d": "2024-01-01", "c": 150.0},
        {"d": "2024-01-02", "c": 152.5},
        {"d": "2024-01-03", "c": 151.0},
        {"d": "2024-01-04", "c": 155.0},
        {"d": "2024-01-05", "c": 158.0},
        {"d": "2024-01-08", "c": 156.5},
        {"d": "2024-01-09", "c": 160.0},
        {"d": "2024-01-10", "c": 162.5},
        {"d": "2024-01-11", "c": 161.0},
        {"d": "2024-01-12", "c": 165.0},
    ]
    
    renderer = TimeSeriesChartRenderer(width=760, height=320)
    
    # Render with different periods
    for period in ["5D", "1M"]:
        svg = renderer.render(data, period=period, title=f"AAPL Price History ({period})")
        print(f"\nPeriod {period}:")
        print(svg[:300] + "...")


def example_custom_keys():
    """Example: Using custom date/value keys."""
    
    print("\n" + "=" * 60)
    print("CUSTOM KEYS EXAMPLE")
    print("=" * 60)
    
    data = [
        {"date": "2024-01-01", "price": 100.0},
        {"date": "2024-01-02", "price": 102.5},
        {"date": "2024-01-03", "price": 101.2},
    ]
    
    renderer = SparklineRenderer()
    svg = renderer.render(data, date_key="date", value_key="price")
    print("\nCustom keys (date, price):")
    print(svg[:200] + "...")


def example_normalization():
    """Example: Data normalization utilities."""
    
    print("\n" + "=" * 60)
    print("DATA NORMALIZATION EXAMPLE")
    print("=" * 60)
    
    data = [
        {"d": "2024-01-01", "c": 100.0},
        {"d": "2024-01-02", "c": 102.5},
        {"d": "2024-01-03", "c": 101.2},
    ]
    
    normalized = normalize_timeseries_data(data)
    print("\nNormalized data:")
    for item in normalized:
        print(f"  {item}")
    
    from timeseries_svg import extract_values, extract_dates
    values = extract_values(normalized)
    dates = extract_dates(normalized)
    
    print(f"\nValues: {values}")
    print(f"Dates: {dates}")


def example_custom_styling():
    """Example: Custom styling options."""
    
    print("\n" + "=" * 60)
    print("CUSTOM STYLING EXAMPLE")
    print("=" * 60)
    
    data = [100.0, 102.5, 101.2, 105.0, 103.8, 107.0]
    
    # Custom sparkline colors
    renderer = SparklineRenderer(
        width=120,
        height=30,
        up_color="#00ff00",
        down_color="#ff0000",
        stroke_width=2.5,
    )
    svg = renderer.render(data)
    print("\nCustom sparkline styling:")
    print(svg[:200] + "...")
    
    # Custom chart colors
    chart_renderer = TimeSeriesChartRenderer(
        width=800,
        height=400,
        up_color="#00aa00",
        down_color="#aa0000",
        grid_color="rgba(200,200,200,0.5)",
    )
    chart_svg = chart_renderer.render(data, period="1M")
    print("\nCustom chart styling:")
    print(chart_svg[:300] + "...")


if __name__ == "__main__":
    example_sparkline()
    example_chart()
    example_custom_keys()
    example_normalization()
    example_custom_styling()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
