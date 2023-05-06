class A:
    def __init__(self) -> None:
        self.__a = 10
        self._b = 20


class B:
    def __init__(self) -> None:
        A.__init__(self)
        print(self.__a)


a = B()