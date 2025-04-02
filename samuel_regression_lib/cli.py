"""
Command-line interface for Samuel Regression Testing Library.

This is the ONLY way for users to add reference data to the database.
"""

import argparse
import sys
import os
import time
from .db import Database
from .extractors import XMLExtractor


def add_reference_data(filepath, method):
    """
    Add reference data to the database for future testing.

    Args:
        filepath: Path to the XML file
        method: Method name (e.g., "lq")

    Returns:
        Success status message
    """
    db = Database()
    extractor = XMLExtractor()

    # First check database connection
    if not db.test_connection():
        return "Error: Database connection failed. Cannot add reference data."

    try:
        with open(filepath, 'r') as f:
            xml_data = f.read()

        filename = os.path.basename(filepath)  # Extract just the filename from path

        # Extract and validate output data
        try:
            output_data = extractor.extract_output(xml_data)
        except Exception as e:
            return f"Error: Could not extract output data from file: {str(e)}"

        print(f"Extracted output data from '{filename}'")

        # Store in database
        print(f"Storing reference data for '{filename}' with method '{method}'...")
        success = db.store_reference_data(filename, method, xml_data, output_data)

        if success:
            return f"Successfully added reference data for '{filename}' with method '{method}'"
        else:
            return f"Failed to add reference data for '{filename}' with method '{method}'"
    except FileNotFoundError:
        return f"Error: File '{filepath}' not found"
    except PermissionError:
        return f"Error: Permission denied when accessing file '{filepath}'"
    except Exception as e:
        return f"Error adding reference data: {str(e)}"


def list_references(method=None):
    """
    List all reference data in the database, optionally filtered by method.

    Args:
        method: Optional method name to filter by

    Returns:
        List of reference data entries
    """
    db = Database()

    # Check connection
    if not db.test_connection():
        return "Error: Database connection failed. Cannot list references."

    try:
        references = db.list_reference_data(method)

        if not references:
            if method:
                return f"No reference data found for method '{method}'"
            else:
                return "No reference data found in the database"

        # Format the output
        result = "Reference data in database:\n"
        result += "----------------------------\n"

        for ref in references:
            created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ref['created_at']))
            result += f"Filename: {ref['filename']}\n"
            result += f"Method: {ref['method']}\n"
            result += f"Created: {created}\n"
            result += "----------------------------\n"

        return result
    except Exception as e:
        return f"Error listing reference data: {str(e)}"


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Samuel Regression Testing Library CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Add reference data command
    add_parser = subparsers.add_parser("add-reference", help="Add reference data to the database")
    add_parser.add_argument("filepath", help="Path to the XML file")
    add_parser.add_argument("method", help="Method name (e.g., 'lq')")

    # List reference data command
    list_parser = subparsers.add_parser("list", help="List reference data in the database")
    list_parser.add_argument("--method", "-m", help="Filter by method name")

    args = parser.parse_args()

    if args.command == "add-reference":
        if not os.path.isfile(args.filepath):
            print(f"Error: File '{args.filepath}' does not exist or is not accessible")
            sys.exit(1)

        result = add_reference_data(args.filepath, args.method)
        print(result)

    elif args.command == "list":
        result = list_references(args.method if hasattr(args, 'method') else None)
        print(result)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()