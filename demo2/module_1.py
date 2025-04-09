class A:
    def __init__(self):
        self.name = "Class A"

    def greet(self, punctuation="!"):
        return f"Hello from {self.name}{punctuation}"

def foo(verbose=False):
    a = A()
    message = a.greet("!!!")
    if verbose:
        print(f"[DEBUG] {message}")
    return message