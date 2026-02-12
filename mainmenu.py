from msvcrt import getwch
from os import system, name
from user_signon import UserSignOn as uso
from typing import Callable



clear_console = lambda: system('cls' if name == 'nt' else 'clear')

class MainMenu:
    def __init__(self, jobs: list[Callable[[], None]] = [exit, exit, exit, exit, exit]):
        self.account_type = 'user' 
        self.jobs = jobs
        self._job_map = {"1. View Inventory": self.jobs[0],
                     "2. Check-in Item": self.jobs[1],
                     "3. Check-out Item": self.jobs[2],
        }
    
    def sign_in(self):
        while True:
            clear_console()
            account = uso().sign_on()

            if account[0] == 'admin':
                self.account_type = account[0]
                self._job_map.update({"4. Add Employee": self.jobs[3],
                                    "5. Terminate Employee": self.jobs[4]})
                
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
        emp = self.sign_in()
        clear_console()
        print(f"Welcome, {emp.name}!")
        selection = self.select_option()
        clear_console()
        if selection == 0:
            print("Viewing Inventory...")

        elif selection == 1:
            print("Checking-in Item...")
        elif selection == 2:
            print("Checking-out Item...")
        elif selection == 3 and self.account_type == 'admin':
            print("Adding Employee...")
        elif selection == 4 and self.account_type == 'admin':
            print("Terminating Employee...")
        elif (selection == 5 and self.account_type == 'admin') or (selection == 3 ):
            print("Exiting...")
            exit()
            

if __name__ == "__main__":
    menu = MainMenu()
    menu.process_selection()