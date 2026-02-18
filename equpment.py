from data_io import DataIO as dio
from time import sleep
from sys import stdout
from msvcrt import kbhit

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
    
    def notify_checkout(self, emp_id: str):
        items = dio().checked_out_items(emp_id) if dio().checked_out_items(emp_id) else None
        items_checked_out: list[str] = []
        if items:
            print(f"You have the following items(s) checked out")
            print(f"{'Name':<55} | {'Qty':>3}") 
            for item in items:
                items_checked_out.append(f"{item[0]:<55} |{item[1]:>3}")
            
            print("\n".join(items_checked_out))
        
        
    
    def checkout(self, employee_id: str):
        while True:
            
            try:
                self.identifier = input("Enter the item identifier to check out: ")
            except ValueError as e:
                print(e)
                continue
            choice = input(f"Confirm checkout of '{self._name}' (ID: {self._id})? (y/n): ").strip().lower()
            if choice == 'y':
                try:
                    dio().checkout_item(self._id, employee_id)
                    print(f"Item '{self._name}' (ID: {self._id}) checked out successfully.")
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
            choice = input(f"Confirm return of '{self._name}' (ID: {self._id})? (y/n): ").strip().lower()
            if choice == 'y':
                try:
                    updated = dio().return_item(self._id, employee_id)
                    if updated:
                        print(f"Item '{self._name}' (ID: {self._id}) returned successfully.")
                    else:
                        print(f"Failed to return item '{self._name}' (ID: {self._id}).")
                except ValueError as e:
                    print(e)
            else:
                print("Return cancelled.")
            break

    def view_inventory(self):
        print("Press any key to stop scrolling through the inventory...")
        items = dio().get_all_items()
        display_list: list[str] = []
        print("ID: | Name                                                    | Qty")
        while True:
            
            for item in items:

                item = (f"{item[0]:>3} | {item[1]:<55} | {item[2]:>3}")
            
                display_list.append(item)
                if kbhit():  
                        return
                if len(display_list) < 30:
                    continue
        
                if len(display_list) == 30:
                    print(f"\n".join(display_list))
                else:
                    display_list.pop(0)
                    stdout.write(f"\033[30A")  # Move cursor up by specified lines
                    stdout.flush()
                    print("\n".join(display_list))
                    
                sleep(0.5)


        
if __name__ == "__main__":
    equipment = Equipment()
    equipment.view_inventory()