#!/usr/bin/env python3
from rich.prompt import Prompt
from cmd_ui import cmd

def main():
    try:
        cmd.login_systeme()
        cmd.afficher_aide()
        
        while True:
            command = Prompt.ask("\n[bold red]root@GuardiaBox[/bold red][white]~[/white] ").strip().lower()

            if command == "exit": break
            elif command == "clear": cmd.afficher_header()
            elif command == "add": cmd.add()
            elif command == "get": cmd.get()
            elif command == "delete": cmd.delete()
            elif command == "list": cmd.list()
            elif command == "help": cmd.afficher_aide()

    except KeyboardInterrupt:
        print("\nDéconnexion...")

if __name__ == "__main__":
    main()