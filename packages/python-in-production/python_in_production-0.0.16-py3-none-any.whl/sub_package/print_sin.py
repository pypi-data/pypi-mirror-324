# import sys  # noqa
# print(sys.path)  # noqa

# sys.path.insert(0, "/home/apalaskos/Documents/On-GitHub/python-packaging")  # noqa

from rich import print

from src.define_xy import my_sin

x, y = my_sin()
print(f"x: {x}")
print(f"y: {y}")
