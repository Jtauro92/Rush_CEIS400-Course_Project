from employee import Employee
from data_io import DataIO


class UserSignOn:
    def __init__(self):
        self.emp = Employee()
        self.dio = DataIO()
        self.admin_account = self.dio.is_admin
        self.id_exist = self.dio.employee_exists
        self.name_exist = self.dio.employee_exists



    def _confirm_id(self):
        while True:
            try:
                self.emp.id = input("Enter your ID: ")
            except ValueError as e:
                print(e)
                continue
            if not self.id_exist(self.emp.id):
                print("Employee ID does not exist. Please try again.")
                continue
            break
        while True:
            try:
                self.emp.name = input("Enter your name: ")
            except ValueError as e:
                print(e)
                continue
            if not self.name_exist(self.emp.name):
                print("Employee name does not exist. Please try again.")
                continue
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