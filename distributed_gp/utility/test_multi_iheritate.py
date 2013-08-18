class A(object):
    def _do(self):
        print '123'


class B(object):
    def _do(self):
        print '321'


class C(B, A):
    def __init__(self):
        B._do(self)
		

