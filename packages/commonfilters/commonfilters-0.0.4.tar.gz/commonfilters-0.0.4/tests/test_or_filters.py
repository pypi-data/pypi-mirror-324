import pytest
from commonfilters import Filter, Filters, OrFilters


def test_or_filters_init():
    filters = OrFilters()
    assert isinstance(filters, Filters)

@pytest.mark.parametrize(
    'value, _filters, expected_result',
    [
        (1, [Filter(lambda x: x == 2), Filter(lambda x: isinstance(x, int))], True),
        (1, [Filter(lambda x: x == 2), Filter(lambda x: isinstance(x, str))], False),
    ],
)
def test_or_filters_filtering(value, _filters, expected_result):
    filters = OrFilters()
    for index, _filter in enumerate(_filters):
        filters[str(index)] = _filter
    assert filters.apply(value) == expected_result
