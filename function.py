"""
alphabet = ["a", "b", "c", "d", "d"]
print(alphabet.index("a"))
print(alphabet.count("d"))

list = [1, 10, 2, 20]
list.sort()
print(list)

list = ["あ", "い", "う", "え", "お"]
list.reverse()
print(list)

def sing():
    print("歌います！")
sing()

def introduce(n):
    print(n + "です")
introduce("Yamada")

def cube_cal(n):
    print(n ** 3)
cube_cal(2)

def introduce(n, age):
    print(n + "です" + str(age) + "歳です")
introduce("Yamada", 19)

def introduce(age, n = "Yamada"):
    print(n + "です" + str(age) + "歳です")
introduce(19)

def introduce(first = "Yamada", second = "Taro"):
    return "名字は" + first + "で、名前は" + second + "です"
print(introduce("Suzuki"))

def cal_bmi(weight, height):
    return weight / (height ** 2)
print(cal_bmi(70, 1.76))

import time
now_time = time.time()
print(now_time)

from time import time
now_time = time()
print(now_time)

class MyProduct:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
        self.sales = 0
    #仕入れメソッド
    def buy_up(self, n):
        self.stock += n
    #売却メソッド
    def sell(self, n):
        self.stock -= n
        self.sales = self.price * n
    #概要メソッド
    def summary(self):
        message = "called summary().\n name: " + self.name + "\n price: " + str(self.price) + "\n stock: " +str(self.stock) + "\n sales: " +str(self.sales)
        print(message)
    #return name
    def get_name(self):
        return self.name
    #discount
    def discount(self, n):
        self.price -= n    
#product1 = MyProduct("phone", 30000, 100)
#product1.discount(5000)
#product1.sell(5)
#product1.summary()

#MyProduct(親クラス)の継承
class MyProductSalesTax(MyProduct):
    def __init__(self, name, price, stock, tax_rate):
        super().__init__(name, price, stock)
        self.tax_rate = tax_rate
    def get_name(self):
        return self.name + "（税込）"
    def get_price_with_tax(self):
        return int(self.price * (1 + self.tax_rate))
    def summary(self):
        message = "called summary().\n name: " + product2.get_name() + "\n price: " + str(product2.get_price_with_tax()) + "\n stock: " +str(self.stock) + "\n sales: " +str(self.sales)
        print(message)
product2 = MyProductSalesTax("phone", 30000, 100, 0.1)
#print(product2.get_name())
#print(product2.get_price_with_tax())
product2.summary()

pai = 3.141592
print("円周率は%f" % pai)
print("円周率は%.3f" % pai)

def bmi(weight, height):
    return weight / height**2
print("bmiは%.4f" % bmi(68, 1.76))

def check_character(object, character):
    return object.count(character)
print(check_character([1, 2, 4, 5, 5, 3], 5))
"""
def binary_search(numbers, target_number):
    #最小値ぎめ
    low = 0;
    high = len(numbers)

    while low <= high:
        #中央値
        middle = (low + high) // 2
        if target_number == numbers[middle]:
            print("{}は{}番目にあります".format(target_number, middle+1))
            break
        elif target_number > numbers[middle]:
            low = middle + 1
        else:
            high = middle - 1
        
        if low > high:
            print(str(target_number) + "は存在しません")

#探索データ
numbers = [2, 4, 6, 57, 23, 86, 1, 3, 5, 36, 47, 20, 38, 11]
#探索する値
target_number = 10
numbers.sort()
print(numbers)
binary_search(numbers, target_number)