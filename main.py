"""Main entry point for Project Jaguar CLI and application execution."""

import sys
from typing import List, Optional
from agents.shell_system import ShellSystem
from config import Config


def main(argv: Optional[List[str]] = None) -> int:
    """Main application entry point supporting interactive REPL or direct arguments."""
    args = argv if argv is not None else sys.argv[1:]
    shell = ShellSystem()

    if args:
        command_str = " ".join(args)
        result = shell.execute_command(command_str)
        if result.content:
            print(result.content)
        return 0 if result.success else 1
    
    print("Starting Project Jaguar Interactive Shell...")
    print("Type 'help' for available commands or 'exit' to quit.")
    
    while True:
        try:
            user_input = input("jaguar> ").strip()
            if not user_input:
                continue
            result = shell.execute_command(user_input)
            if result.content:
                print(result.content)
            if result.metadata and result.metadata.get("should_exit"):
                break
        except (KeyboardInterrupt, EOFError):
            print("\nExiting session.")
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
