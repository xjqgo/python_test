class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclasses should implement this method")


class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"


class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"


def animal_sound(animal):
    # 这里体现了多态，不同的 Animal 子类对象调用 speak 方法会有不同的行为
    print(animal.speak())


dog = Dog("Buddy")
cat = Cat("Kitty")

# 调用 animal_sound 函数，传入不同的 Animal 子类对象
animal_sound(dog)
animal_sound(cat)