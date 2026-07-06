class Test:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
t : Test = Test("Nam",12)
print(f"truoc khi setattr : {t.name},{t.age}")
setattr(t,"name","Hoang")
setattr(t,"age",100)
print(f"sau khi setattr : {t.name},{t.age}")

setattr(t,"con_chim",100)
print(hasattr(t,"con_chim"))
