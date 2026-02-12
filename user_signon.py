from employee import Employee
from data_io import DataIO


class UserSignOn:
    def __init__(self):
        self.emp = Employee()
        self.admin_account = DataIO().is_admin
        self.id_exist = DataIO().employee_exists
        self.name_exist = DataIO().employee_exists



    def _confirm_id(self):
        while True:
            self.emp.id = input("Enter your ID: ")
            if self.id_exist(self.emp.id):
                print(False)
            self.emp.name = input("Enter your name: ")
            if not self.name_exist(self.emp.name):
                raise ValueError("Invalid name entered.")
            return self.emp

                
    
    def sign_on(self) -> tuple[str, Employee]:
        try:
            employee = self._confirm_id()
        except ValueError as ve:
            raise ve
        if self.admin_account(self.emp.id):
            try:
                self.emp.pswd = input("Enter your password: ")
                return 'admin', employee
            except ValueError as ve:
                raise ve
        return 'user', employee
  
            

    

if __name__ == "__main__":
    user_signon = UserSignOn()
    result = user_signon.sign_on()
    if result and result[0] == 'admin':
        print("Admin access granted.")