class Repiater:
    def echo[T](self, x: T) -> T:
        return x


def f(x, y):
    return x.echo(y)


r = Repiater()
a = f(r, 1)  # : int
b = f(r, "one")  # : int | str, but if previous line is removed : str
