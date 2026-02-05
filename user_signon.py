from typing import Optional
from employee import Employee
from data_io import DataIO

class UserSignOn:
    def __init__(self):
        self.emp = Employee()
        self.admin_account = DataIO().is_admin



    def _confirm_id(self):

        self.emp.id = input("Enter your ID: ")
        self.emp.name = input("Enter your name: ")

                
    
    def sign_on(self) -> Optional[bool]:
        while True:
            try:
                self._confirm_id()
            except ValueError as ve:
                print(ve)
                continue
            if self.admin_account(self.emp.id):
                try:
                    self.emp.pswd = input("Enter your password: ")
                    return True
                except ValueError as ve:
                    print(ve)
                    continue
            break

    

if __name__ == "__main__":
    user_signon = UserSignOn()
    user_signon.sign_on()
    if user_signon.admin_account(user_signon.emp.id):
        print("Admin access granted.")