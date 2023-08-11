

class parent:
    def parent_func(self):
        print("EGGS")

class child:
    def child_func(self, test_func=self.parent_func):
        self.parent_func()
        

c = child()
c.child_func()
