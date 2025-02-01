# anymethod
> @anymethod = instance method + @classmethod

[![license](https://img.shields.io/github/license/makukha/anymethod.svg)](https://github.com/makukha/anymethod/blob/main/LICENSE)
[![pypi](https://img.shields.io/pypi/v/anymethod.svg#v0.1.2)](https://pypi.python.org/pypi/anymethod)
[![python versions](https://img.shields.io/pypi/pyversions/anymethod.svg)](https://pypi.org/project/anymethod)
[![tests](https://raw.githubusercontent.com/makukha/anymethod/v0.1.2/docs/badge/tests.svg)](https://github.com/makukha/anymethod)
[![coverage](https://raw.githubusercontent.com/makukha/anymethod/v0.1.2/docs/badge/coverage.svg)](https://github.com/makukha/anymethod)
[![tested with multipython](https://img.shields.io/badge/tested_with-multipython-x)](https://github.com/makukha/multipython)
[![uses docsub](https://img.shields.io/badge/uses-docsub-royalblue)](https://github.com/makukha/docsub)

For the cases when class and its instances can be used interchangeably, code duplication can be avoided if the same member function works both as `@classmethod` and instance method.

This can be easily achieved with Python [descriptors](https://docs.python.org/3/howto/descriptor.html).


## Installation

```shell
$ pip install anymethod
```


## Example A

<!-- docsub: begin -->
<!-- docsub: include tests/mypy/test_exampleA.txt -->
<!-- docsub: lines after 1 upto -1 -->
```dectest
>>> from anymethod import anymethod

>>> class FooBar:
...     @anymethod
...     def whoami[O](owner: O) -> O:
...         return owner

>>> FooBar.whoami()
<class '__main__.FooBar'>

>>> FooBar().whoami()
<__main__.FooBar object at 0x...>
```
<!-- docsub: end -->


## Example B

<!-- docsub: begin -->
<!-- docsub: include tests/mypy/exampleB.py -->
<!-- docsub: lines after 1 upto -1 -->
```python
from typing import Any, ClassVar
from anymethod import anymethod


class FooBar:
    _cls: ClassVar[list[Any]] = []
    _obj: list[Any]

    def __init__(self) -> None:
        self._obj = []

    @anymethod
    def add_value(owner, v: Any) -> None:
        if isinstance(owner, type):
            owner._cls.append(v)
        else:
            owner._obj.append(v)
```
<!-- docsub: end -->


## More info

Check the [Project changelog](https://github.com/makukha/anymethod/tree/main/CHANGELOG.md)
