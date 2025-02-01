from typing import Union, List, Optional
import pandas as pd
from datetime import datetime


def get_date_format(date_str: str) -> tuple[Optional[str], Optional[str]]:
    """
    Determines the date format of a given string.

    Args:
        date_str: The date string to analyze

    Returns:
        tuple: (format_type: str, format_string: str) or (None, None) if invalid
    """
    date_str = str(date_str).strip()

    formats = [
        ("YYYY-MM-DD", "%Y-%m-%d", 10),
        ("YYYY-MM", "%Y-%m", 7),
        ("YYYY-Q[1-4]", "quarter", 7),
        ("YYYY", "%Y", 4),
    ]

    for format_name, fmt, length in formats:
        if len(date_str) != length:
            continue

        if fmt == "quarter":
            if date_str[4] == "-" and date_str[5] == "Q" and date_str[6] in "1234" and date_str[:4].isdigit():
                return format_name, fmt
        else:
            try:
                if fmt == "%Y":
                    year = int(date_str)
                    if 1900 <= year <= datetime.now().year:
                        return format_name, fmt
                else:
                    datetime.strptime(date_str, fmt)
                    return format_name, fmt
            except ValueError:
                continue

    return None, None


def validate_date_format(date_str: str, format_type: str, format_string: str) -> bool:
    """
    Validates if a date string matches the expected format.

    Args:
        date_str: The date string to validate
        format_type: The expected format type
        format_string: The format string pattern

    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(date_str, str):
        return False

    date_str = date_str.strip()

    if format_type == "YYYY-Q[1-4]":
        return (
            len(date_str) == 7
            and date_str[4] == "-"
            and date_str[5] == "Q"
            and date_str[6] in "1234"
            and date_str[:4].isdigit()
            and 1900 <= int(date_str[:4]) <= datetime.now().year
        )

    try:
        if format_string == "%Y":
            year = int(date_str)
            return 1900 <= year <= datetime.now().year
        else:
            datetime.strptime(date_str, format_string)
            return True
    except ValueError:
        return False


def validate_linechart_df(df, validate_dates: bool = True) -> tuple[bool, Optional[str]]:
    """
    Validates line chart data according to specification.

    Args:
        data: List of lists containing the chart data
        validate_dates: Whether to perform date validation (default True)

    Returns:
        tuple: (is_valid: bool, error_message: Optional[str])
    """
    try:
        # 1. Basic DataFrame Structure Validation
        if df.empty:
            return False, "DataFrame cannot be empty"

        if len(df.columns) < 2:
            return False, "Must have at least 2 columns (date + 1 data series)"

        if len(df.columns) > 11:
            return False, "Cannot have more than 11 columns (date + 10 series)"

        if len(df) < 2:
            return False, "Must have at least 2 rows of data"

        if len(df) > 3000:
            return False, "Cannot exceed 3,000 rows"

        # 2. Basic Null Validation
        if df.isna().all(axis=1).any():
            return False, "Contains completely null rows"

        if df.isna().all().any():
            return False, "Contains completely null columns"

        # 3. Total Cells Validation
        total_cells = len(df) * len(df.columns)
        if total_cells > 11000:
            return False, "Total cells cannot exceed 11000"

        # 4. Type Validation for Non-Date Columns
        numeric_cols = df.iloc[:, 1:]
        non_null_numeric = numeric_cols.dropna()

        if not non_null_numeric.stack().map(lambda x: isinstance(x, (int, float))).all():
            return False, "All non-date values must be numeric (int or float) or null"

        # 5. Date Column Validation
        if validate_dates:
            date_col = df.iloc[:, 0]

            # Determine format from first row
            first_date = str(date_col.iloc[0])
            format_type, format_string = get_date_format(first_date)

            if format_type is None:
                return False, f"Invalid date format in first row: {first_date}"

            # Validate all dates match the determined format
            if not all(validate_date_format(str(d), format_type, format_string) for d in date_col):
                better_validation_message = (
                    f"Since the first date was of type {format_type}, dates must match format {format_type}"
                )
                return False, better_validation_message

            # Basic year validation
            years = [int(str(d)[:4]) for d in date_col]
            if any(y < 1900 or y > datetime.now().year for y in years):
                return False, "Dates must be between 1900 and current year"

            # Check for duplicates and order
            if date_col.duplicated().any():
                return False, "Contains duplicate dates"

            if not date_col.is_monotonic_increasing:
                return False, "Dates are not in ascending order"

        # First/last row nulls
        if numeric_cols.iloc[0].isna().all() or numeric_cols.iloc[-1].isna().all():
            return False, "First or last row contains all null values"

        return True, None

    except Exception as e:
        return False, f"Validation error: {str(e)}"
