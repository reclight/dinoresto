class Person:
  def __init__(self, ame, age):
    self.name = ame
    self.age = age

  def change(self, ame):
    self.name=ame

  def myfunc(self):
    self.change("abcd")
    print("Hello my name is " + self.name)

p1 = Person("John", 36)
p1.change("abc")
p1.myfunc()
