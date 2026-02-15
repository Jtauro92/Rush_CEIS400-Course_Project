from data_io import DataIO as dio

class Equipment:
    def __init__(self):
        self._identifier = ''
        self._item = None
        self._id = ''
        self._name = ''
        self._quantity = 0


    @property
    def item(self):
        return self._item
    
    @item.setter
    def item(self):
        if not dio().item_exists(self._identifier):
            raise ValueError("Item does not exist.")
        self._item = dio().get_item(self._identifier)
        if self._item:
            self._id = self._item[0]
            self._name = self._item[1]
            self._quantity = self._item[2]
    
    @property
    def identifier(self):
        return self._identifier
    
    @identifier.setter
    def identifier(self, value: str):
        if value.isnumeric() and not (0 < int(value) <= 100):
            raise ValueError("Item does not exist.")
        self._identifier = value
        self._item = dio().get_item(self._identifier) if dio().item_exists(self._identifier) else None
        if self._item:
            self._id = self._item[0]
            self._name = self._item[1]
            self._quantity = self._item[2]
        else:
            raise ValueError("Item does not exist.")
        
        
    
    def checkout(self, employee_id: str):
        while True:
            
            try:
                self.identifier = input("Enter the item identifier to check out: ")
            except ValueError as e:
                print(e)
                continue

            try:
                dio().checkout_item(self._id, employee_id)
            except ValueError as e:
                print(e)
            break

    def return_item(self, employee_id: str):
        while True:
            try:
                self.identifier = input("Enter the item identifier to return: ")

            except ValueError as e:
                print(e)
                continue

            try:
                dio().return_item(self._id, employee_id)
            except ValueError as e:
                print(e)
            break
    
if __name__ == "__main__":
    equipment = Equipment()
    equipment.checkout('12345')