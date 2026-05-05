import easy_shopping

print(easy_shopping.calculator.addition(7,5))
print(easy_shopping.calculator.subtraction(34,21))
print(easy_shopping.calculator.multiplication(54,2))
print(easy_shopping.calculator.division(144,2))
print(easy_shopping.calculator.division(45,0))

newCart = easy_shopping.shopping.shoppingCart()

newCart.addItems(["apple","rice","toothbrush"])
print(newCart.items)
print(newCart.getTotalAmount())

newCart.removeItem("rice")
print(newCart.items)
print(newCart.getTotalAmount())