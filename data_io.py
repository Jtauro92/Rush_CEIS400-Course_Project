from sqlite3 import Connection, Error
from sql_quieries import CREATE_TABLE, ADD_EMPLOYEE, IS_ADMIN

DATABASE = 'inventory.db'

class DataIO(Connection):

    def __init__(self):
        try:
            super().__init__(DATABASE, autocommit=True)
        except Error as e:
            print(f"Error connecting to database: {e}")

        self.cursor = self.cursor()

    def _execute_query(self, query: str, params: tuple = ()):
        try:
            self.cursor.execute(query, params)
        except Error as e:
            raise RuntimeError(f"Database query error: {e}")
        
    def _fetch_all(self, query: str, params: tuple = ()) -> list[tuple]:
        self._execute_query(query, params)
        return self.cursor.fetchall()
    
    def _fetch_one(self, query: str, params: tuple = ()) -> tuple:
        self._execute_query(query, params)
        return self.cursor.fetchone()
    
    def _create_table(self):
        self._execute_query(CREATE_TABLE)

    def employee_exists(self, identifier) -> bool:
        query = "SELECT 1 FROM employees WHERE id = ? or name = ? LIMIT 1;"
        result = self._fetch_one(query, (identifier, identifier))
        return result is not None

    def add_employee(self, name: str, id: str):
        with self:
            self._create_table()
            self._execute_query(ADD_EMPLOYEE, (id, name))


    def is_admin(self, id: str) -> bool:
        result = self._fetch_one(IS_ADMIN, (id,))
        return result is not None and result[0] == 'yes'
    
    def get_password(self, id: str) -> str:
        query = "SELECT password FROM employees WHERE id = ? AND admin = 'yes';"
        return self._fetch_one(query, (id,))[0]


if __name__ == "__main__":
    data_io = DataIO()
    print(data_io.add_employee("Jane Doe", "123467"))  