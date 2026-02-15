CREATE_TABLE = """
                CREATE TABLE IF NOT EXISTS employees (
                id TEXT PRIMARY KEY,
                admin TEXT DEFAULT NULL,
                name TEXT NOT NULL,
                password TEXT DEFAULT NULL
                );"""

ADD_EMPLOYEE = """
                INSERT INTO employees (id, name) VALUES (?, ?);"""

IS_ADMIN = """
                SELECT admin FROM employees WHERE id = ?;"""

GET_PASSWORD = """
                SELECT password FROM employees WHERE id = ? AND admin = ?
                ;"""

CREATE_EQUIPMENT_TABLE = """
                CREATE TABLE IF NOT EXISTS equipment (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL);"""

CREATE_CHECKOUT_TABLE = """
                CREATE TABLE IF NOT EXISTS checkouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT NOT NULL,
                equipment_id TEXT NOT NULL UNIQUE,
                checkout_date DATE DEFAULT CURRENT_DATE,
                return_date DATE DEFAULT NULL,
                check_in_date DATE DEFAULT NULL,
                quantity INTEGER DEFAULT 0,
                FOREIGN KEY (employee_id) REFERENCES employees(id),
                FOREIGN KEY (equipment_id) REFERENCES equipment(id)
                );""" 