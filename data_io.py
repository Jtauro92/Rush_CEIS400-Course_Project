from sqlite3 import Connection, Error
from sql_quieries import CREATE_TABLE, CREATE_CHECKOUT_TABLE, CREATE_EQUIPMENT_TABLE, ADD_EMPLOYEE, IS_ADMIN
from typing import Optional
from datetime import date


DATABASE = 'inventory.db'

class DataIO(Connection):

    def __init__(self):
        try:
            super().__init__(DATABASE, autocommit=True)
        except Error as e:
            print(f"Error connecting to database: {e}")

        self.return_date = str(date.today().replace(day=date.today().day + 7)) #7 days from checkout date format: YYYY-MM-DD
        self._create_table()
    
    def _create_table(self):
        self.cursor().execute(CREATE_TABLE)
        self.cursor().execute(CREATE_EQUIPMENT_TABLE)
        self.cursor().execute(CREATE_CHECKOUT_TABLE)

    def employee_exists(self, identifier: str) -> bool:
        query = "SELECT 1 FROM employees WHERE id = ? OR name = ? LIMIT 1;"
        result = self.cursor().execute(query, (identifier, identifier))
        result = result.fetchone()
        return result is not None

    def item_exists(self, identifier: str) -> bool:
        query = "SELECT 1 FROM equipment WHERE id = ? OR name = ? LIMIT 1;"
        result = self.cursor().execute(query, (identifier, identifier))
        result = result.fetchone()
        return result is not None
    
    def return_item(self, identifier: str, employee_id: str):
        if not self.item_exists(identifier):
            raise ValueError(f"Item with ID or name '{identifier}' does not exist.")
        query = "UPDATE equipment SET quantity = quantity + 1 WHERE id = ? OR name = ?;"
        self.cursor().execute(query, (identifier, identifier))
        query = f"""UPDATE checkouts
                    SET return_date = CURRENT_DATE
                    WHERE employee_id = {employee_id}
                    AND equipment_id = ?
                    AND return_date IS NULL;"""
        self.cursor().execute(query, (identifier,))
        if not self.item_exists(identifier):
            raise ValueError(f"Item with ID or name '{identifier}' does not exist.")
        query = "UPDATE equipment SET quantity = quantity - 1 WHERE id = ? OR name = ?;"
        self.cursor().execute(query, (identifier, identifier))
        query = """INSERT INTO checkouts (employee_id, equipment_id, checkout_date, return_date) 
                   VALUES (?, (SELECT id FROM equipment WHERE id = ? OR name = ?), CURRENT_TIMESTAMP, ?);"""
        self.cursor().execute(query, (employee_id, identifier, identifier, self.return_date))
    
    def add_employee(self, name: str, id: str):
        with self:
            self._create_table()
            self.cursor().execute(ADD_EMPLOYEE, (id, name))
        
    def delete_employee(self, id: str):
        with self:
            if self.is_admin(id):
                raise ValueError("Cannot terminate an admin employee.")
            query = "DELETE FROM employees WHERE id = ? and admin IS NULL;"
            self.cursor().execute(query, (id,))

    def is_admin(self, id: str | int) -> bool:
        result = self.cursor().execute(IS_ADMIN, (id,))
        result = result.fetchone()
        return result is not None and result[0] == 'yes'
    
    def get_password(self, id: str | int) -> Optional[str]:
        query = "SELECT password FROM employees WHERE id = ? AND admin = 'yes';"
        result = self.cursor().execute(query, (id,))
        result = result.fetchone()
        return result[0] if result is not None else None


if __name__ == "__main__":
    with DataIO() as d:
        print(d.employee_exists("Jason Rush"))