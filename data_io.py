from sqlite3 import Connection, Error
from sql_quieries import CREATE_TABLE, CREATE_CHECKOUT_TABLE, CREATE_EQUIPMENT_TABLE, ADD_EMPLOYEE, IS_ADMIN
from typing import Optional
import csv
import random

DATABASE = 'inventory.db'

class DataIO(Connection):

    def __init__(self):
        try:
            super().__init__(DATABASE, autocommit=True)
        except Error as e:
            print(f"Error connecting to database: {e}")

        self.cursor().execute("PRAGMA foreign_keys = ON;")

        self._create_table()
    
    def _create_table(self):
        with self:
            self.cursor().execute(CREATE_TABLE)
            self.cursor().execute(CREATE_EQUIPMENT_TABLE)
            self.populate_equipment()
            self.cursor().execute(CREATE_CHECKOUT_TABLE)

    def populate_equipment(self):
        with open("products.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            try:
                for row in reader:
                    query = "INSERT INTO equipment (id, name, quantity) VALUES (?, ?, ?);"
                    self.cursor().execute(query, (row["Index"], row["Name"], random.randint(1, 100)))
            except Error:
                    pass

    def employee_exists(self, identifier: str) -> bool:
        query = "SELECT 1 FROM employees WHERE id = ? OR name = ? LIMIT 1;"
        with self:
            result = self.cursor().execute(query, (identifier, identifier))
            result = result.fetchone()
        return result is not None
    
    def admin_employee_exists(self) -> bool:
        query = "SELECT 1 FROM employees WHERE admin = 'yes' LIMIT 1;"
        with self:
            result = self.cursor().execute(query)
            result = result.fetchone()
        return result is not None

    def item_exists(self, identifier: str) -> bool:
        query = "SELECT 1 FROM equipment WHERE id = ? OR name = ? LIMIT 1;"
        with self:
            result = self.cursor().execute(query, (identifier, identifier))
            result = result.fetchone()
        return result is not None
    
    def get_item(self, identifier: str) -> tuple[str, str, int] | None:
        query = "SELECT id, name, quantity FROM equipment WHERE id = ? OR name = ? LIMIT 1;"
        with self:
            result = self.cursor().execute(query, (identifier, identifier))
            result = result.fetchone()
        return result if result is not None else None
    
    def get_all_items(self) -> list[tuple[str, str, int]]:
        query = """SELECT id, name, quantity FROM equipment;"""
        with self:
            result = self.cursor().execute(query)
            return result.fetchall()
            
    
    def return_item(self, item_id: str, employee_id: str):
        update_quantity = f"""UPDATE equipment 
                            SET quantity = quantity + 1 
                            WHERE id = '{item_id}';"""
        
        update_record = f"""UPDATE checkouts 
                        SET quantity = quantity - 1, check_in_date = CURRENT_DATE
                        WHERE rowid = (
                        SELECT rowid FROM checkouts
                        WHERE employee_id = '{employee_id}' AND equipment_id = '{item_id}' 
                        AND return_date IS NOT NULL
                        ORDER BY checkout_date ASC
                        LIMIT 1
                    );"""
        
        with self:
            self.cursor().execute(update_quantity)
            result = self.cursor().execute(update_record)
            return result.rowcount > 0  # Return True if a record was updated, False otherwise
        

    def checkout_item(self, item_id: str, employee_id: str):
        update_quantity = f"""UPDATE equipment 
                            SET quantity = quantity - 1 
                            WHERE id = '{item_id}' AND quantity > 0;"""
        
        # Check for open checkout from TODAY
        checkout_record = f"""SELECT 1 FROM checkouts
                            WHERE employee_id = '{employee_id}' AND equipment_id = '{item_id}' 
                            AND date(checkout_date) = CURRENT_DATE;"""
        
        update_record = f"""UPDATE checkouts 
                            SET quantity = quantity + 1
                            WHERE employee_id = '{employee_id}' AND equipment_id = '{item_id}'
                            AND date(checkout_date) = CURRENT_DATE;"""
        
        insert_record = f"""INSERT INTO checkouts (employee_id, equipment_id, checkout_date, return_date, quantity)
                            VALUES ('{employee_id}', '{item_id}', CURRENT_DATE, date('now', '+7 days'), 1)
                            ;"""
        with self:
            result =self.cursor().execute(update_quantity)
            if result.rowcount == 0:
                raise ValueError("Item is out of stock.")
            
            result = self.cursor().execute(checkout_record)
            if result.fetchone() is not None:
                self.cursor().execute(update_record)  # Update today's checkout
            else:
                self.cursor().execute(insert_record)   # Insert new (not today's)

                
    def add_employee(self, name: str, id: str):
        with self:
            self._create_table()
            self.cursor().execute(ADD_EMPLOYEE, (id, name))

    def add_admin_employee(self, name: str, id: str, password: str):
        with self:
            self._create_table()
            query = """INSERT INTO employees (id, name, admin, password) 
            VALUES (?, ?, 'yes', ?);"""
            self.cursor().execute(query, (id, name, password))
        
    def delete_employee(self, id: str):
        with self:
            if self.is_admin(id):
                raise ValueError("Cannot terminate an admin employee.")
            query = "DELETE FROM employees WHERE id = ? and admin IS NULL;"
            self.cursor().execute(query, (id,))

    def is_admin(self, id: str | int) -> bool:
        result = self.cursor().execute(IS_ADMIN, (id,))
        with self:
            result = result.fetchone()
            return result is not None and result[0] == 'yes'
    
    def get_password(self, id: str | int) -> Optional[str]:
        query = "SELECT password FROM employees WHERE id = ? AND admin = 'yes';"
        result = self.cursor().execute(query, (id,))
        result = result.fetchone()
        return result[0] if result is not None else None
    
    def checked_out_items(self, employee_id: str) -> list[tuple[str, str]] | None:
        query = """SELECT e.name, c.quantity
                FROM checkouts AS c
                JOIN equipment AS e ON e.id = c.equipment_id
                WHERE c.employee_id = ? AND c.quantity > 0;"""
        result = self.cursor().execute(query, (employee_id,))
        result = result.fetchall()
        return result if len(result) > 0 else None


if __name__ == "__main__":
    with DataIO() as d:
        print(d.populate_equipment())