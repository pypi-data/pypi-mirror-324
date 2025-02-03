import os
import shutil
import sys
import subprocess
import sqlite3
from colorama import Fore, init

init(autoreset=True)

def create_app(name):
    try:
        os.makedirs(name)

        # Create important directory for activepy.py
        important_dir = os.path.join(name, 'important')
        os.makedirs(important_dir)

        # Create activepy.py inside the important directory
        activepy_content = """import sqlite3
from colorama import Fore, Style

class Activepy:
    def __init__(self):
        self.conn = None

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
"""

        activepy_path = os.path.join(important_dir, 'activepy.py')
        with open(activepy_path, 'w') as activepy_file:
            activepy_file.write(activepy_content)

        # Create scripts directory and empty script.py file
        scripts_dir = os.path.join(name, 'scripts')
        os.makedirs(scripts_dir)
        script_path = os.path.join(scripts_dir, 'script.py')
        with open(script_path, 'w') as script_file:
            pass  # Create an empty script.py file

        # Create settings directory and file
        settings_dir = os.path.join(name, 'settings')
        os.makedirs(settings_dir)

        settings_content = """# settings.py

HTML_FILE = 'index.html'
PORT = 8000
"""
        settings_path = os.path.join(settings_dir, 'settings.py')
        with open(settings_path, 'w') as settings_file:
            settings_file.write(settings_content)

        # Create templates directory and HTML file
        templates_dir = os.path.join(name, 'templates')
        os.makedirs(templates_dir)
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
</head>
<body>
    <h1>Welcome to your Activepy app!</h1>
</body>
</html>
"""
        html_path = os.path.join(templates_dir, 'index.html')
        with open(html_path, 'w') as html_file:
            html_file.write(html_content)

        # Create manage.py file
        manage_content = """import os
import http.server
import socketserver
from settings.settings import HTML_FILE, PORT
from colorama import Fore

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        try:
            template_path = os.path.join('templates', HTML_FILE)
            with open(template_path, 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            print(f"{Fore.RED}[Err.01] Template '{HTML_FILE}' not found!")
            self.wfile.write(b"File not found!")

def main():
    os.chdir(os.path.dirname(__file__))

    html_file_path = os.path.join('templates', HTML_FILE)
    if not os.path.exists(html_file_path):
        print(f"{Fore.RED}[Err.01] Template '{HTML_FILE}' not found! Server will not start.")
        return

    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server running on http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
"""
        manage_path = os.path.join(name, 'manage.py')
        with open(manage_path, 'w') as manage_file:
            manage_file.write(manage_content)

        # Create models directory and sample model file
        models_dst = os.path.join(name, 'models')
        os.makedirs(models_dst)
        model_content = """# Sample model file
class SampleModel:
    pass
"""
        with open(os.path.join(models_dst, 'sample_model.py'), 'w') as model_file:
            model_file.write(model_content)

        print(f"{Fore.GREEN}✅ App '{name}' created successfully, with manage.py, settings, templates, scripts, models, and activepy.py in the important directory.")
    except FileExistsError:
        print(f"{Fore.RED}❌ Error: The app '{name}' already exists.")
    except Exception as e:
        print(f"{Fore.RED}❌ Error during app creation: {e}")

def delete_app(name):
    app_path = os.path.join(os.getcwd(), name)
    if os.path.exists(app_path):
        shutil.rmtree(app_path)
        print(f"{Fore.GREEN}✅ App '{name}' deleted successfully.")
    else:
        print(f"{Fore.RED}❌ Error: The app '{name}' does not exist.")

def create_database(app_name, db_name):
    db_path = os.path.join(os.getcwd(), app_name, f"{db_name}.db")
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.close()
        print(f"{Fore.GREEN}✅ Database '{db_name}' created successfully for app '{app_name}'.")
    else:
        print(f"{Fore.RED}❌ Error: Database '{db_name}' already exists.")

def delete_database(app_name, db_name):
    db_path = os.path.join(os.getcwd(), app_name, f"{db_name}.db")
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"{Fore.GREEN}✅ Database '{db_name}' deleted successfully from app '{app_name}'.")
    else:
        print(f"{Fore.RED}❌ Error: Database '{db_name}' does not exist.")

def start_app(name):
    app_path = os.path.join(os.getcwd(), name)
    if os.path.exists(app_path):
        os.chdir(app_path)
        subprocess.run(["python", "manage.py"])
    else:
        print(f"{Fore.RED}❌ Error: The app '{name}' does not exist.")

def main():
    if len(sys.argv) < 3:
        print("Need help? See the documentation at https://activepy.tiiny.site")
        return

    command = sys.argv[1]
    name = sys.argv[2]

    if command == "createapp":
        create_app(name)
    elif command == "startapp":
        start_app(name)
    elif command == "deleteapp":
        delete_app(name)
    elif command == "createdatabase":
        if len(sys.argv) != 4:
            print(f"{Fore.RED}❌ Usage: actpy createdatabase [appname] [databasename]")
            return
        create_database(sys.argv[2], sys.argv[3])
    elif command == "deletedatabase":
        if len(sys.argv) != 4:
            print(f"{Fore.RED}❌ Usage: actpy deletedatabase [appname] [databasename]")
            return
        delete_database(sys.argv[2], sys.argv[3])
    elif command == "help" or command == "documentation":
        print("Documentation: https://activepy.tiiny.site")
    else:
        print(f"{Fore.RED}❌ Unrecognized command.")

if __name__ == "__main__":
    main()