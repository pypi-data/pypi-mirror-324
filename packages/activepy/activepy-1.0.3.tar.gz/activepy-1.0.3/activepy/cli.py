import os
import shutil
import sys
import subprocess
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def create_app(name):
    """Creates a folder for the app with the specified name and copies manage.py and the models folder."""
    try:
        # Create the directory for the new app
        os.makedirs(name)

        # Copy the manage.py file from the templates folder
        src_file = os.path.join(os.path.dirname(__file__), '..', 'templates', 'manage.py')
        dst_file = os.path.join(name, 'manage.py')
        shutil.copy(src_file, dst_file)

        # Copy the models folder from the templates folder
        models_src = os.path.join(os.path.dirname(__file__), '..', 'templates', 'models')
        models_dst = os.path.join(name, 'models')
        shutil.copytree(models_src, models_dst)

        print(f"{Fore.GREEN}✅ App '{name}' created successfully, and manage.py and the models folder have been copied.")
    except FileExistsError:
        print(f"{Fore.RED}❌ Error: The app '{name}' already exists.")
    except Exception as e:
        print(f"{Fore.RED}❌ Error during app creation: {e}")

def start_app(name):
    """Runs the manage.py file of the specified app."""
    try:
        app_path = os.path.join(os.getcwd(), name)
        manage_file = os.path.join(app_path, 'manage.py')

        if not os.path.exists(manage_file):
            print(f"{Fore.RED}❌ Error: The manage.py file does not exist in the '{name}' folder.")
            return

        # Execute the manage.py file
        subprocess.run(['python', manage_file])
        print(f"{Fore.GREEN}✅ Execution of manage.py completed successfully.")
    except Exception as e:
        print(f"{Fore.RED}❌ Error during the execution of manage.py: {e}")

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 3:
        print("Usage: actpy [createapp|start] [name]")
        return

    command = sys.argv[1]
    name = sys.argv[2]

    if command == "createapp":
        create_app(name)
    elif command == "start":
        start_app(name)
    else:
        print(f"{Fore.RED}❌ Unrecognized command.")

if __name__ == "__main__":
    main()