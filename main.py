import calculator
import shopping

print(calculator.addition(7,5))
print(calculator.subtraction(34,21))
print(calculator.multiplication(54,2))
print(calculator.division(144,2))
print(calculator.division(45,0))

newCart = shopping.shoppingCart()

newCart.addItems(["apple","rice","toothbrush"])
print(newCart.items)
print(newCart.getTotalAmount())

newCart.removeItem("rice")
print(newCart.items)
print(newCart.getTotalAmount())
