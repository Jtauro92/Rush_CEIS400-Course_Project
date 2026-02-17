from data_io import DataIO

class Employee:
    def __init__(self, name: str = '', id: str = '0'):
        self._name = name
        self._id = id
        self._pswd = ''

        self.emp_exists = DataIO().employee_exists
        self.get_password = DataIO().get_password
        self.add_record = DataIO().add_employee
        self.delete_record = DataIO().delete_employee

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        if value.isnumeric():
            raise ValueError("Employee name cannot be numeric.")
        if value.strip() == '':
            raise ValueError("Employee name cannot be empty.")  
        self._name = value.title()
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value: str):
        if not value.isnumeric():
            raise ValueError("Employee ID must be numeric.")
        if len(value) != 5:
            raise ValueError("Employee ID must be exactly 5 digits long.")
        self._id = value

    @property
    def pswd(self):
        return self._pswd
    
    @pswd.setter
    def pswd(self, value: str):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        if value != self.get_password(self._id):
            raise ValueError("Incorrect password.")
        self._pswd = True

    def add_employee_record(self):
        while True:
            try:
                self.id = input("Enter Employee ID: ")
            except ValueError as e:                
                print(e)
                continue        
            if self.emp_exists(self._id):
                print("Employee ID already exists. Please try again.")
                continue
            break
        while True:
            try:
                self.name = input("Enter Employee Name: ")
            except ValueError as e:
                print(e)
                continue
            break
        self.add_record(self.name, self.id)
        print(f"Employee '{self.name}' with ID {self.id} added successfully.")



    def delete_employee_record(self):
        while True:
            try:
                self.id = input("Enter Employee ID to delete: ")
            except ValueError as e:
                print(e)
                continue
            if not self.emp_exists(self._id):
                print("Employee ID does not exist. Please try again.")
                continue
            break
        self.delete_record(self._id)
        print(f"Employee with ID {self.id} deleted successfully.")

    def __str__(self):
        return f"Employee(Name: {self._name}, ID: {self._id})"
    
if __name__ == "__main__":
    emp = Employee()
    emp.add_employee_record()
