import os
import shutil
import sys
import subprocess
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

def create_app(name):
    """Creates a folder for the app with the specified name and writes manage.py, settings, and templates."""
    try:

        os.makedirs(name)

        settings_dir = os.path.join(name, 'settings')
        os.makedirs(settings_dir)


        settings_content = """# settings.py

# Name of the file in the templates folder that will be executed at the start of the app.
HTML_FILE = 'index.html'
# More features will  be added in the future.
"""
        settings_path = os.path.join(settings_dir, 'settings.py')
        with open(settings_path, 'w') as settings_file:
            settings_file.write(settings_content)


        templates_dir = os.path.join(name, 'templates')
        os.makedirs(templates_dir)
        html_content = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
</head>
<body>
    <h1>Welcome to your app Activepy!</h1>
</body>
</html>
"""
        html_path = os.path.join(templates_dir, 'index.html')
        with open(html_path, 'w') as html_file:
            html_file.write(html_content)

        manage_content = """import os
import http.server
import socketserver
from settings.settings import HTML_FILE
from colorama import Fore

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    \"\"\"Handler per gestire le richieste HTTP.\"\"\"
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # Serve the HTML file
        try:
            template_path = os.path.join('templates', HTML_FILE)
            with open(template_path, 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            print(f"{Fore.RED}[Err.01] Template '{HTML_FILE}' not found!")
            self.wfile.write(b"File not found!")

def main():
    \"\"\"Avvia il server HTTP.\"\"\"
    os.chdir(os.path.dirname(__file__))
    
    # Check if the HTML file exists before starting the server
    html_file_path = os.path.join('templates', HTML_FILE)
    if not os.path.exists(html_file_path):
        print(f"{Fore.RED}[Err.01] Template '{HTML_FILE}' not found! Server will not start.")
        return

    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server avviato su http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
"""
        manage_path = os.path.join(name, 'manage.py')
        with open(manage_path, 'w') as manage_file:
            manage_file.write(manage_content)

        # Create models directory and a placeholder model file
        models_dst = os.path.join(name, 'models')
        os.makedirs(models_dst)
        model_content = """# Sample model file
class SampleModel:
    pass
"""
        with open(os.path.join(models_dst, 'sample_model.py'), 'w') as model_file:
            model_file.write(model_content)

        print(f"{Fore.GREEN}✅ App '{name}' created successfully, with manage.py, settings, templates, and models directory.")
    except FileExistsError:
        print(f"{Fore.RED}❌ Error: The app '{name}' already exists.")
    except Exception as e:
        print(f"{Fore.RED}❌ Error during app creation: {e}")

def start_app(name):
    """Starts an existing app given its name."""
    app_path = os.path.join(os.getcwd(), name)
    if os.path.exists(app_path):
        os.chdir(app_path)
        subprocess.run(["python", "manage.py"])
    else:
        print(f"{Fore.RED}❌ Error: The app '{name}' does not exist.")

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 3:
        print("Usage: actpy [createapp|startapp] [name]")
        return

    command = sys.argv[1]
    name = sys.argv[2]

    if command == "createapp":
        create_app(name)
    elif command == "startapp":
        start_app(name)
    else:
        print(f"{Fore.RED}❌ Unrecognized command.")

if __name__ == "__main__":
    main()