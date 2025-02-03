import sqlite3
from colorama import Fore, Style

class Activepy:
    def __init__(self):
        self.conn = None
        self.current_db = None

    def connectdatabase(self, db_name):
        db_path = f"{db_name}.db"
        self.conn = sqlite3.connect(db_path)
        print(f"{Fore.GREEN}[INFO] Connected to database: {db_name}{Style.RESET_ALL}")

    def createtabe(self, table_name):
        if self.conn is not None:
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);"
            self.conn.execute(sql)
            self.conn.commit()
            print(f"{Fore.GREEN}[INFO] Table '{table_name}' created successfully.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[ERROR] No database connected.{Style.RESET_ALL}")

    def readdata(self, table_name):
        if self.conn is not None:
            cursor = self.conn.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            return rows
        else:
            print(f"{Fore.RED}[ERROR] No database connected.{Style.RESET_ALL}")
            return []

    def addata(self, table_name, data):
        if self.conn is not None:
            placeholders = ', '.join(['?'] * len(data))
            sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
            self.conn.execute(sql, data)
            self.conn.commit()
            print(f"{Fore.GREEN}[INFO] Data added to {table_name}: {data}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[ERROR] No database connected.{Style.RESET_ALL}")

    def removedata(self, table_name, condition):
        if self.conn is not None:
            sql = f"DELETE FROM {table_name} WHERE {condition}"
            self.conn.execute(sql)
            self.conn.commit()
            print(f"{Fore.GREEN}[INFO] Data removed from {table_name} where {condition}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[ERROR] No database connected.{Style.RESET_ALL}")

    def close(self):
        if self.conn:
            self.conn.close()
            print(f"{Fore.GREEN}[INFO] Database connection closed.{Style.RESET_ALL}")

# Create a global instance of Activepy
activepy = Activepy()