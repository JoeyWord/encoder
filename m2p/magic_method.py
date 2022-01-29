# encoding=utf-8

class A(object):
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.ls = []
        self.ls.extend([key,value])
        self.index = 0
        self.max_iter = 10
    
    def __str__(self):
        return "key={} and value={}".format(self.key,self.value)
    
    def __len__(self):
        return len(self.ls)
    
    def __call__(self,a):
        if a>1:
            return self.value*a
        return self.value
    def __cmp__(self,other):
        if self.value == other.value:
            return cmp(self.key,other.value)
        return -cmp(self.value,other.value)

    #设置实例的属性，对实例属性赋值时自动调用，不可以使用self.a=key设置，会陷入max deep recursion
    def __setattr__(self,a,val):
        if a == 'score':
            raise ValueError("invalid score setting")
        elif val == 'age':
            raise ValueError("no suit data set")
        elif val == 'name':
            print("change the value")
            self.name = 'doudou'
    #获取实例属性，对属性访问时调用。在构造函数属性访问时就生成
    def __getattr__(self,a):
        return 'right'
    
    def __iter__(self):
        pass
    
    def __next__(self):
        if self.index >= self.max_iter:
            raise StopIteration
        while True:
            self.index += 1
            return list(range(self.max_iter))[self.index]
    
if __name__ == "__main__":
    a=A('a',3)
    print("a:{}".format(a))
    print("a length={}".format(len(a)))
    print("a multiply:{}".format(a(2)))
    a2=A('b',2)
    a3=A('b',4)
    _ls = [a,a2,a3]
    print(sorted(_ls))
    a.value = 6
    print("a attr value={}".format(a.value))
    print("value:",a.value)
    a.value = 100 