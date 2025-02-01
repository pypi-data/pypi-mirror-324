# richset

[![Python](https://img.shields.io/pypi/pyversions/richset.svg)](https://badge.fury.io/py/richset)
[![PyPI version](https://img.shields.io/pypi/v/richset.svg)](https://pypi.python.org/pypi/richset/)
[![codecov](https://codecov.io/gh/kitsuyui/python-richset/branch/main/graph/badge.svg?token=LH210UT9Q0)](https://codecov.io/gh/kitsuyui/python-richset)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

richset interporlates with set, dict, and list.

## Motivations and Concepts

- richset provides useful functions for common use cases of set, dict, and list.
- builtin set, dict and list requires many boilerplate codes.
- Pure Python package.
- Fully typing supported.
- No magic. No meta-programming.

## Install

```sh
$ pip install richset
```

## Usage

```python
from dataclasses import dataclass
from richset import RichSet


@dataclass(frozen=True)
class Something:
    id: int
    name: str


richset = RichSet.from_list([
    Something(1, 'one'),
    Something(2, 'two'),
    Something(3, 'three'),
])
```

### Conversions

```python
richset.to_list()  # => [Something(1, 'one'), Something(2, 'one'), Something(3, 'three')]
richset.to_tuple()  # => (Something(1, 'one'), Something(2, 'two'), Something(3, 'three'))
richset.to_set()  # => {Something(1, 'one'), Something(2, 'two'), Something(3, 'three')}
richset.to_frozenset()  # => frozenset({Something(1, 'one'), Something(2, 'two'), Something(3, 'three')})
richset.to_dict(lambda s: s.id)  # => {1: Something(1, 'one'), 2: Something(2, 'two'), 3: Something(3, 'three')}
```

`to_dict()` takes second argument `duplicated` which is a choice of `'error'`, `'first'` or `'last'`.

- if `duplicated` is `'error'`, then `to_dict()` raises `ValueError` if there is a duplicated key.
- if `duplicated` is `'first'`, then `to_dict()` picks the first one of duplicated key.
- if `duplicated` is `'last'`, then `to_dict()` picks the last one of duplicated key.

`to_dict_of_list()` is similar to `to_dict()` but it returns a dict of list.

```python
richset.to_dict_of_list(lambda s: s.name)  # => {'john': [Something(1, 'john'), Something(2, 'john')], 'jane': [Something(3, 'jane')]}
```

### List accessors

```python
richset.first()  # => returns first item `Something(1, 'one')` or raise Error (if empty)
richset.get_first()  # => returns first item `Something(1, 'one')` or None (if empty)
richset.last()  # => returns last item `Something(3, 'three')` or raise Error (if empty)
richset.get_last()  # => returns last item `Something(3, 'three')` or None (if empty)
richset.nth(2)  # => returns 3rd item `Something(3, 'three')` or raise Error (if empty)
richset.get_nth(2)  # => returns 3rd item `Something(3, 'three')` or None (if empty)
richset.one()  # => returns one item `Something(1, 'one')` or raise Error (if empty)
richset.get_one()  # => returns one item `Something(1, 'one')` or None (if empty)
```

Note: `get_first`, `get_last`, `get_nth` and `get_one` accept `default` argument that returns specified value instead of None.

```python
richset.get_nth(100, default=Something(-1, 'default'))  # => Something(-1, 'default')
```

### List basic manipulations

```python
richset.pushed(Something(4, 'four')).to_list()  # => [Something(1, 'one'), Something(2, 'two'), Something(3, 'three'), Something(4, 'four')]
richset.unshift(Something(4, 'four')).to_list()  # => [Something(4, 'four'), Something(1, 'one'), Something(2, 'two'), Something(3, 'three')]
richset.popped()  # => Something(3, 'three'), RichSet([Something(1, 'one'), Something(2, 'two')])
richset.shift()  # => Something(1, 'one'), RichSet([Something(2, 'two'), Something(3, 'three')])
richset.slice(1, 2).to_list()  # => [Something(2, 'two')]
richset.divide_at(1)  # => RichSet([Something(1, 'one')]), RichSet([Something(2, 'two'), Something(3, 'three')])
```

- `pushed_all()` and `unshift_all()` are similar to `pushed()` and `unshift()` but they accept multiple items.
- `popped_n()` and `shift_n()` are similar to `popped()` and `shift()` but they accept count of items.

### List functional manipulations

```python
richset.unique(lambda s: s.id)  # => unique by id
richset.map(lambda s: s.id).to_list()  # => [1, 2]
richset.filter(lambda s: s.id > 1).to_list()  # => [Something(2, 'two'), Something(3, 'three')]
```

### Search

```python
richset.index(lambda s: s.id == 2)  # => 1
richset.indices(lambda s: s.id == 2)  # => [1]
richset.search_first(lambda s: s.id == 2)  # => Something(2, 'two')
richset.search_last(lambda s: s.id == 2)  # => Something(2, 'two')
richset.search_all(lambda s: s.id == 2)  # => [Something(2, 'two')]
richset.contains(lambda s: s.id == 2)  # => True
richset.has(Something(2, 'two'))  # => True
```

### Sorts

```python
richset.sorted(key=lambda s: s.name, reverse=True).to_list()  # => [Something(2, 'two'), Something(3, 'three'), Something(1, 'one')]
richset.reversed().to_list()  # => [Something(3, 'three'), Something(2, 'two'), Something(1, 'one')]
```

### Statistics

```python
richset.is_empty()  # => True if empty
richset.is_not_empty()  # => True if not empty
richset.size()  # => 3
richset.count(lambda s: s.id > 1)  # => 2
```

### Set operations

```python
richset = RichSet.from_list([
    Something(3, 'three'),
    Something(4, 'four'),
    Something(5, 'five'),
])
richset2 = RichSet.from_list([
    Something(3, 'three'),
    Something(4, 'four'),
    Something(6, 'six'),
])
```

```python
richset.union(richset2).to_set()  # => {Something(3, 'three'), Something(4, 'four'), Something(5, 'five'), Something(6, 'six')}
richset.intersection(richset2).to_set()  # => {Something(3, 'three'), Something(4, 'four')}
richset.difference(richset2).to_set()  # => {Something(5, 'five')}
richset.symmetric_difference(richset2).to_set()  # => {Something(5, 'five'), Something(6, 'six')}
richset.cartesian_product(richset2).to_set()  # => {(Something(3, 'three'), Something(3, 'three')), (Something(3, 'three'), Something(4, 'four')), (Something(3, 'three'), Something(6, 'six')), (Something(4, 'four'), Something(3, 'three')), (Something(4, 'four'), Something(4, 'four')), (Something(4, 'four'), Something(6, 'six')), (Something(5, 'five'), Something(3, 'three')), (Something(5, 'five'), Something(4, 'four')), (Something(5, 'five'), Something(6, 'six'))}
richset.zip(richset2).to_set()  # => {(Something(3, 'three'), Something(3, 'three')), (Something(4, 'four'), Something(4, 'four')), (Something(5, 'five'), Something(6, 'six')}
```

Also `is_subset()`, `is_superset()`, `is_disjoint()`, `is_equal_as_set()` and `zip_longest()` are available.

### Grouping

```python
richset.group_by(lambda item: item.id % 2)  # => {1: RichSet(records=(Something(id=1, name='one'), Something(id=3, name='three'))), 0: RichSet(records=(Something(id=2, name='two'),))}
richset.size_of_group_by(lambda item: item.id % 2)  # => {1: 2, 0: 1}
richset.count_of_group_by(key=lambda item: item.id % 2, predicate=lambda item: item.name.startswith('t'))  # => {1: 1, 0: 1}
richset.aggregate_by(key=lambda r: r.id % 2, fn=lambda a, b: a + b.name, initial='')  # => {1: 'onethree', 0: 'two'}
```

## Paging

```python
richset.page(1, 2).to_list()  # => [Something(1, 'one'), Something(2, 'two')]
richset.split_into_pages(2).to_list()  # => [RichSet([Something(1, 'one'), Something(2, 'two')]), RichSet([Something(3, 'three')])]
```

# LICENSE

The 3-Clause BSD License. See also LICENSE file.
