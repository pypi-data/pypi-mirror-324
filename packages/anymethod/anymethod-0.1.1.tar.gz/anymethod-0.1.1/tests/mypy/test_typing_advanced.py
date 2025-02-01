from anymethod import anymethod


class A:
    @anymethod
    def whoami[O](owner: O) -> O:
        # assert_type(owner, Self | type[Self])  # todo: must pass
        return owner


class B(A): ...


def test_typing() -> None:
    a = A()
    b = B()

    assert A.whoami() is A
    # assert_type(A.whoami(), type[A])  # todo: must pass

    assert a.whoami() is a
    # assert_type(a.whoami(), A)  # todo: must pass

    assert B.whoami() is B
    # assert_type(B.whoami(), type[B])  # todo: must pass

    assert b.whoami() is b
    # assert_type(b.whoami(), B)  # todo: must pass
