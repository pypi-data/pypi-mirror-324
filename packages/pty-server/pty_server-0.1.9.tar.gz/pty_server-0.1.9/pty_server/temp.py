class Test:
    def __init__(self):
        self.a = 1

    def __enter__(self):
        self.a = 2
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(exc_value)
        self.a = 3
        print(self.a)



with Test() as t:
    print(t.a)
    raise Exception("Hello")