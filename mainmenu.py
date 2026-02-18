from msvcrt import getwch
from os import system, name
from typing import Callable
from user_signon import UserSignOn as uso
from time import sleep
from employee import Employee as e
from equpment import Equipment as eq


clear_console = lambda: system('cls' if name == 'nt' else 'clear')

class MainMenu:
    def __init__(self):
        self.account_type = 'user' 
        
        self._job_map : dict[str, Callable[..., None]] = {"1. View Inventory": eq().view_inventory,
                                                        "2. Return Item": eq().return_item,
                                                        "3. Check-out Item": eq().checkout,
        }
    
    def sign_in(self):
        while True:
            clear_console()
            print("Please sign in to continue...")
            account = uso().sign_on()

            if account[0] == 'admin':
                self.account_type = account[0]
                self._job_map.update({"4. Add Employee": e().add_employee_record,
                                    "5. Terminate Employee": e().delete_employee_record})
                
            self._job_map.update({"0. Exit": exit})
            return account[1]


    def __str__(self):
        clear_console()

        menu_str = "Admin Menu:\n" if self.account_type == 'admin' else "Main Menu:\n"
        
        menu_str += '\n'.join(self._job_map.keys())
        return menu_str
            
    def select_option(self):
        def navigation():
                key = getwch()  # Get the actual key code
                if key == 'H':
                    return 'up'
                elif key == 'P':
                    return 'down'
                elif key == '\r':
                    return '\r'        
        index = 0
        jobs_list = list(self._job_map.keys())
        while True:
            
            menu_str = "Admin Menu:\n" if self.account_type == 'admin' else "Main Menu:\n"
            for i, job in enumerate(jobs_list):
                if i == index:
                    menu_str += f"> {job} <\n"
                else:
                    menu_str += f"{job}\n"
            clear_console()
            print(menu_str.rstrip())
            action = navigation()

            if action == 'up' and index > 0:
                index -= 1
            elif action == 'down' and index < len(jobs_list) - 1:
                index += 1
            if action == '\r':
                return index

    def process_selection(self):
        e().add_admin_employee_record()
        sleep(2)
        emp = self.sign_in()
        clear_console()
        print(f"Welcome, {emp.name}!")
        eq().notify_checkout(emp.id)
        sleep(2)
        while True:
            selection = self.select_option()
            clear_console()
            if selection == 0:
                print("Viewing Inventory...")
                self._job_map["1. View Inventory"]()

            elif selection == 1:
                print("Checking-in Item...")
                self._job_map["2. Return Item"](emp.id)
                sleep(2)

            elif selection == 2:
                print("Checking-out Item...")
                self._job_map["3. Check-out Item"](emp.id)
                sleep(2)

            elif selection == 3 and self.account_type == 'admin':
                print("Adding Employee...")
                self._job_map["4. Add Employee"]()
                sleep(2)

            elif selection == 4 and self.account_type == 'admin':
                print("Terminating Employee...")
                self._job_map["5. Terminate Employee"]()
                sleep(2)

            elif (selection == 5 and self.account_type == 'admin') or (selection == 3 ):
                print("Exiting...")
                self._job_map["0. Exit"]()
                break
            

if __name__ == "__main__":
    menu = MainMenu()
    menu.process_selection()