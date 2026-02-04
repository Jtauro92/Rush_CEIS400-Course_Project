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