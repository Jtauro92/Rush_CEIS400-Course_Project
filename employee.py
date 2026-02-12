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
        if not value.isnumeric():
            self._name = value.title()
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value: str):
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
        self.id = input("Enter Employee ID: ")
        if self.emp_exists(self._id):
            raise ValueError(f"Employee with ID {self._id} already exists.")
        self.name = input("Enter Employee Name: ")
        self.add_record(self.name, self.id)


    def delete_employee_record(self):
        while True:
            self.id = input("Enter Employee ID to Terminate: ")
            try:
                self.delete_record(self.id)
            except ValueError as e:
                print(e)
                continue
            print(f"Employee with ID {self.id} has been terminated.")
            break

    def __str__(self):
        return f"Employee(Name: {self._name}, ID: {self._id})"
    
if __name__ == "__main__":
    emp = Employee()
    emp.add_employee_record()
