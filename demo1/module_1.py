# NOTE: This file uses updated code from module_1.py
class A:
    def __init__(self):
        self.name = "Class A"

    def greet(self):
        return f"Hello from {self.name}"

def foo():
    a = A()
    return a.greet()

