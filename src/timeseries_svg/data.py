"""Data normalization utilities for time series data."""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime


def normalize_timeseries_data(
    data: Any,
    date_key: str = "d",
    value_key: str = "c",
    date_format: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Normalize various JSONB input formats into a standard time series structure.
    
    Supports multiple input formats:
    - List of dicts: [{"d": "2024-01-01", "c": 100.0}, ...]
    - List of lists: [["2024-01-01", 100.0], ...]
    - Dict with date keys: {"2024-01-01": 100.0, ...}
    - List of values (dates auto-generated): [100.0, 101.0, ...]
    
    Args:
        data: Input data in various formats
        date_key: Key name for date in dict format (default: "d")
        value_key: Key name for value in dict format (default: "c")
        date_format: Optional strftime format for date parsing
    
    Returns:
        List of dicts with standardized "date" and "value" keys
    """
    if data is None:
        return []
    
    # List of dicts
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        result = []
        for item in data:
            date_val = _extract_date(item, date_key, date_format)
            value_val = _extract_value(item, value_key)
            if date_val is not None and value_val is not None:
                result.append({"date": date_val, "value": value_val})
        return result
    
    # List of lists/tuples
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], (list, tuple)):
        result = []
        for item in data:
            if len(item) >= 2:
                date_val = _parse_date(item[0], date_format)
                value_val = _parse_value(item[1])
                if date_val is not None and value_val is not None:
                    result.append({"date": date_val, "value": value_val})
        return result
    
    # Dict with date keys
    if isinstance(data, dict):
        result = []
        for date_str, value in data.items():
            date_val = _parse_date(date_str, date_format)
            value_val = _parse_value(value)
            if date_val is not None and value_val is not None:
                result.append({"date": date_val, "value": value_val})
        # Sort by date
        result.sort(key=lambda x: x["date"])
        return result
    
    # List of values (auto-generate dates)
    if isinstance(data, list):
        result = []
        for idx, value in enumerate(data):
            value_val = _parse_value(value)
            if value_val is not None:
                result.append({"date": f"day-{idx}", "value": value_val})
        return result
    
    return []


def _extract_date(item: Dict[str, Any], key: str, date_format: Optional[str]) -> Optional[str]:
    """Extract and normalize date from dict item."""
    date_val = item.get(key)
    return _parse_date(date_val, date_format)


def _extract_value(item: Dict[str, Any], key: str) -> Optional[float]:
    """Extract and normalize value from dict item."""
    value = item.get(key)
    # Auto-detect common aliases if key not found
    if value is None:
        # Try 'v' (value) if looking for 'c' (close)
        if key == "c":
            value = item.get("v")
        # Try 'c' (close) if looking for 'v' (value)
        elif key == "v":
            value = item.get("c")
        # Try 'value' for both
        if value is None:
            value = item.get("value")
    return _parse_value(value)


def _parse_date(value: Any, date_format: Optional[str]) -> Optional[str]:
    """Parse date value into standard ISO format string."""
    if value is None:
        return None
    
    # Already a string
    if isinstance(value, str):
        return value
    
    # Try to parse datetime
    if isinstance(value, datetime):
        return value.isoformat()
    
    # Try to parse from timestamp
    if isinstance(value, (int, float)):
        try:
            dt = datetime.fromtimestamp(value)
            return dt.isoformat()
        except (ValueError, OSError):
            pass
    
    return str(value)


def _parse_value(value: Any) -> Optional[float]:
    """Parse value into float."""
    if value is None:
        return None
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def extract_values(normalized_data: List[Dict[str, Any]]) -> List[float]:
    """Extract just the values from normalized data."""
    return [item["value"] for item in normalized_data if item.get("value") is not None]


def extract_dates(normalized_data: List[Dict[str, Any]]) -> List[str]:
    """Extract just the dates from normalized data."""
    return [item["date"] for item in normalized_data if item.get("date") is not None]
