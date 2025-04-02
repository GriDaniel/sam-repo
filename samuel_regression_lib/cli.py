"""
Command-line interface for the regression testing library.
"""

import argparse
import sys
import os
from . import add_reference_data


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Regression Testing Library CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Add reference data command
    add_parser = subparsers.add_parser("add-reference", help="Add reference data to the database")
    add_parser.add_argument("filepath", help="Path to the XML file")
    add_parser.add_argument("method", help="Method name (e.g., 'lq')")

    args = parser.parse_args()

    if args.command == "add-reference":
        if not os.path.isfile(args.filepath):
            print(f"Error: File '{args.filepath}' does not exist or is not accessible")
            sys.exit(1)

        result = add_reference_data(args.filepath, args.method)
        print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()