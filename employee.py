from data_io import DataIO

class Employee:
    def __init__(self, name: str = '', id: int = 0):
        self._name = name
        self._id = id
        self._pswd = ''

        self.employee_exists = DataIO().employee_exists
        self.get_password = DataIO().get_password

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value.isnumeric():
            value = value.title()
        if not self.employee_exists(value):
            raise ValueError("Employee does not exist in the database.")
        self._name = value
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value: str):
        if not self.employee_exists(value):
            raise ValueError("Employee does not exist in the database.")
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

    def __str__(self):
        return f"Employee(Name: {self._name}, ID: {self._id})"
    
if __name__ == "__main__":
    emp = Employee()
    emp.name = "John Doe"
    print(emp)