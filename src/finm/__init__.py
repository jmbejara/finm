"""
finm - Financial Mathematics Python Package

A student-led Python package for financial mathematics and quantitative finance
education, created by students and educators at the University of Chicago
Financial Mathematics program.

⚠️  DISCLAIMER: This package is for learning purposes only. There are likely
errors and this should NOT be used for any purposes beyond education and research.
"""

from finm.fixedincome import (
    present_value,
    future_value,
    yield_to_maturity,
    bond_price,
    duration,
    modified_duration,
    convexity,
)

__version__ = "0.1.0"
__author__ = "University of Chicago Financial Mathematics Program"

__all__ = [
    "present_value",
    "future_value",
    "yield_to_maturity",
    "bond_price",
    "duration",
    "modified_duration",
    "convexity",
]

