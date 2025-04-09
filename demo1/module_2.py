# NOTE: This file uses updated code from module_2.py
from module_1 import foo

class B:
    def __init__(self):
        self.data = foo()

    def show(self):
        return f"B got message: {self.data}"

def bar():
    b = B()
    return b.show()