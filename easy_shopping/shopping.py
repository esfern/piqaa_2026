class shoppingCart():
    def __init__(self, items = []):
        self.items = items

    # Add one item
    def addItem(self, x):
        return self.items.append(x)
    
    # Add multiple items
    def addItems(self, x):
        return self.items.extend(x)
    
    # Remove items from cart
    def removeItem(self, x):
        return self.items.remove(x)
    
    def getTotalAmount(self):
        return len(self.items)

    