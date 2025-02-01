from anymethod import anymethod


class A:
    @anymethod
    def whoami[O](owner: O) -> O:
        # assert_type(owner, Self | type[Self])  # todo: must pass
        return owner


def test_cls_typing() -> None:
    # assert_type(A.whoami(), type[A])  # todo: must pass
    assert A.whoami() is A


def test_obj_typing() -> None:
    a = A()
    # assert_type(a.whoami(), A)  # todo: must pass
    assert a.whoami() is a
