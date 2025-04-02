"""
Regression testing library for XML-based tests with MongoDB references.
"""

from .cli import add_reference_to_db
from .main import RegressionTest

__all__ = ['RegressionTest', 'add_reference_to_db']