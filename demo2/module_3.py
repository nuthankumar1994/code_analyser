from module_2 import bar

class C:
    def __init__(self):
        self.result = bar()

    def display(self):
        return f"C displays: {self.result}"

def baz():
    c = C()
    return c.display()