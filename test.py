class decorator2:
    
    def __init__(self, f):
        self.f = f
        print("decorator2 object instantiated")
    def __call__(self):
        print("Decorating", self.f.__name__)
        self.f()

@decorator2
def foo2():
    print("Just ran foo2")
    return None

foo2()
