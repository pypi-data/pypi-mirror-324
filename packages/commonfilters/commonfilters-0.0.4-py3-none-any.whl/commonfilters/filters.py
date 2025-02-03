# coding=utf-8
"""
Module of filters
"""

from collections import UserDict, UserList
from typing import Any, Callable, List, Optional, Iterable

from .filter_coupling_policy import FilterCouplingPolicy


class Filters(UserDict):
    """
    Filters collection with AND default coupling policy
    """
    def __init__(self, *args, **kwargs):
        UserDict.__init__(self, *args, **kwargs)
        self.default_coupling_policy = FilterCouplingPolicy.AND

    def apply(
        self,
        value: Any,
        filter_names: Optional[List[str]] = None,
        coupling_policy: Optional[FilterCouplingPolicy] = None,
    ) -> bool:
        """
        Apply all or certain registered filters
        """
        return apply_filters(
            value,
            self.values()
            if filter_names is None
            else [
                self[filter_name]
                for filter_name in filter_names
                if filter_name in self
            ],
            coupling_policy=(
                self.default_coupling_policy
                if coupling_policy is None
                else coupling_policy
            ),
        )

    def apply_and(
        self,
        value: Any,
        filter_names: Optional[List[str]] = None,
    ) -> bool:
        """
        Apply all or certain registered filters with "AND" logic
        """
        return self.apply(value, filter_names, coupling_policy=FilterCouplingPolicy.AND)

    def apply_or(
        self,
        value: Any,
        filter_names: Optional[List[str]] = None,
    ) -> bool:
        """
        Apply all or certain registered filters with "OR" logic
        """
        return self.apply(value, filter_names, coupling_policy=FilterCouplingPolicy.OR)


class OrFilters(Filters):
    """
    Filters collection with OR default coupling policy
    """
    def __init__(self, *args, **kwargs):
        Filters.__init__(self, *args, **kwargs)
        self.default_coupling_policy = FilterCouplingPolicy.OR


class Compounder:
    """
    Class that implement logic of compounding
    """

    def __and__(self, other) -> 'CompoundFilter':
        return CompoundFilter([self, other], coupling_policy=FilterCouplingPolicy.AND)

    def __rand__(self, other) -> 'CompoundFilter':
        return CompoundFilter([other, self], coupling_policy=FilterCouplingPolicy.AND)

    def __or__(self, other) -> 'CompoundFilter':
        return CompoundFilter([self, other], coupling_policy=FilterCouplingPolicy.OR)

    def __ror__(self, other) -> 'CompoundFilter':
        return CompoundFilter([other, self], coupling_policy=FilterCouplingPolicy.OR)


# pylint: disable=too-few-public-methods
class Filter(Compounder):
    """
    Class of single filter
    """

    def __init__(self, validator: Callable, *args, **kwargs):
        self.validator = validator
        self.args = args
        self.kwargs = kwargs

    def apply(self, value: Any) -> bool:
        """
        Apply the filter for given value
        """
        return self.validator(value, *self.args, **self.kwargs)


class CompoundFilter(UserList, Compounder):
    """
    Coupling filters
    """

    def __init__(
        self,
        filters: List['Filter | CompoundFilter'],
        *,
        coupling_policy: FilterCouplingPolicy = FilterCouplingPolicy.AND,
    ):
        super().__init__(filters)
        self.coupling_policy = coupling_policy or FilterCouplingPolicy.AND

    def apply(self, value: Any):
        """
        Apply compound filter
        """
        return apply_filters(value, self, coupling_policy=self.coupling_policy)  # pylint: disable=protected-access


def apply_filters(
    value: Any,
    filters: Iterable['Filter | CompoundFilter'],
    coupling_policy: FilterCouplingPolicy = FilterCouplingPolicy.AND,
) -> bool:
    """
    Apply filters to value
    """
    coupling_policy = coupling_policy or FilterCouplingPolicy.AND
    if coupling_policy == FilterCouplingPolicy.AND:
        return apply_filters_with_and_policy(value, filters)
    if coupling_policy == FilterCouplingPolicy.OR:
        return apply_filters_with_or_policy(value, filters)
    raise NotImplementedError(f'FilterCouplingPolicy ({coupling_policy}) is not supported')


def apply_filters_with_and_policy(
    value: Any,
    filters: Iterable['Filter | CompoundFilter'],
):
    """
    Apply with "AND" logic
    """
    for _filter in filters or []:
        if not _filter.apply(value):
            return False
    return True


def apply_filters_with_or_policy(
    value: Any,
    filters: Iterable['Filter | CompoundFilter'],
):
    """
    Apply with "OR" logic
    """
    if not filters:
        return True
    for _filter in filters:
        if _filter.apply(value):
            return True
    return False
