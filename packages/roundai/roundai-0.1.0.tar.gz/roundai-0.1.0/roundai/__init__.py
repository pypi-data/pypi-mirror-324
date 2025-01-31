"""
RoundAI - A smart rounding library that rounds numbers from right to left.

This library provides an alternative to Python's built-in round() function,
with more intuitive behavior for certain use cases.
"""

from .round import roundai, round_from_right

__version__ = "0.1.0"
__all__ = ["roundai", "round_from_right"]
