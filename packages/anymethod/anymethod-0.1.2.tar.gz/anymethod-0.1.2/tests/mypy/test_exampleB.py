from exampleB import FooBar


def test_exampleB() -> None:
    FooBar.add_value(0)
    foobar = FooBar()
    foobar.add_value(1)

    assert foobar._cls == [0]
    assert foobar._obj == [1]
