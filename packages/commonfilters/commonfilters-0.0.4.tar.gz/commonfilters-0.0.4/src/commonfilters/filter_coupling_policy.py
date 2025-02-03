# coding=utf-8
"""
FilterCouplingPolicy
"""

from enum import StrEnum


class FilterCouplingPolicy(StrEnum):
    """
    Policy of coupling
    """
    AND = 'and'
    OR = 'or'
