

class A():
    "Insight: ⚠️ Affected functions total 2 and they are ['module_1.foo', 'module_2.__init__']): .\n--- demo1/module_1.py\n+++ demo2/module_1.py\n@@ -1 +1 @@\n-# NOTE: This file uses updated code from module_1.py\n+class A:"

    def __init__(self):
        self.name = 'Class A'

    def greet(self, punctuation='!'):
        return f'Hello from {self.name}{punctuation}'

def foo(verbose=False):
    "Insight: ⚠️ Affected functions total 1 and they are ['module_2.__init__']): .\n--- demo1/module_1.py\n+++ demo2/module_1.py\n@@ -1 +1 @@\n-\n+def foo(verbose=False):"
    a = A()
    message = a.greet('!!!')
    if verbose:
        print(f'[DEBUG] {message}')
    return message
