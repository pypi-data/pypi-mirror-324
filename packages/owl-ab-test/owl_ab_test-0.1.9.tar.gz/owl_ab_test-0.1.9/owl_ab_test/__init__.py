"""
owl_ab_test - A Python package for A/B testing statistical analysis
"""

from owl_ab_test.core import calculate_proportion_stats, process_stats, plot_confidence_intervals, calculate_revenue_stats
from owl_ab_test.exceptions import InvalidInputError

__version__ = "0.1.9"
__all__ = ["calculate_proportion_stats",
           "calculate_revenue_stats",
           "InvalidInputError",
           "process_stats",
           "plot_confidence_intervals"]
