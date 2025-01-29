class ziwojs:
    def __init__(self,name,age,tc,ktc):
        print(name)
        print(age)
        print(tc)
        self.ktc=ktc
        self.name=name

    def koutou(self):
        print(self.ktc)


class MyClass:
    def __init__(self, param1, param2):
        # 初始化方法，在创建对象时会自动调用
        # param1 和 param2 是传入的参数
        self.param1 = param1
        self.param2 = param2

    def method1(self):
        # 类的方法，可对对象的属性进行操作或实现某种功能
        print(f"param1 is {self.param1} and param2 is {self.param2}")


# 创建对象
obj = MyClass("value1", "value2")
cxk = ziwojs('蔡徐坤',23,'篮球','你干嘛哎呦')
# 调用对象的方法
obj.method1()
cxk.koutou()
print(cxk.name)