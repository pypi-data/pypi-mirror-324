# anymethod
> @anymethod = instance method + @classmethod

[![license](https://img.shields.io/github/license/makukha/anymethod.svg)](https://github.com/makukha/anymethod/blob/main/LICENSE)
[![pypi](https://img.shields.io/pypi/v/anymethod.svg#v0.1.0)](https://pypi.python.org/pypi/anymethod)
[![python versions](https://img.shields.io/pypi/pyversions/anymethod.svg)](https://pypi.org/project/anymethod)
[![tests](https://raw.githubusercontent.com/makukha/anymethod/v0.1.0/docs/badge/tests.svg)](https://github.com/makukha/anymethod)
[![coverage](https://raw.githubusercontent.com/makukha/anymethod/v0.1.0/docs/badge/coverage.svg)](https://github.com/makukha/anymethod)
[![tested with multipython](https://img.shields.io/badge/tested_with-multipython-x)](https://github.com/makukha/multipython)
[![uses docsub](https://img.shields.io/badge/uses-docsub-royalblue)](https://github.com/makukha/docsub)

For the cases when class and its instances can be used interchangeably, code duplication can be avoided if the same member function works both as `@classmethod` and instance method.

This can be easily achieved with Python [descriptors](https://docs.python.org/3/howto/descriptor.html).


## Usage

```python
from anymethod import anymethod

class FooBar:
    @anymethod
    def who_is_my_owner(owner) -> None:
        print(owner)
```


## Installation

```shell
$ pip install anymethod
```


## Example

<!-- docsub: begin -->
<!-- docsub: include tests/test_usage.txt -->
<!-- docsub: lines after 1 upto -1 -->
```dectest
>>> from anymethod import *

>>> class FooBar:
...     @anymethod
...     def whoami(owner) -> None:
...         me = 'cls' if isinstance(owner, type) else 'obj'
...         print(me, owner)

>>> FooBar.whoami()
cls <class '__main__.FooBar'>

>>> FooBar().whoami()
obj <__main__.FooBar object ...>
```
<!-- docsub: end -->


## More info

Check the [Project changelog](https://github.com/makukha/anymethod/tree/main/CHANGELOG.md)
