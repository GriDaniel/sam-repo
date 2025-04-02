"""
Command-line interface for the regression testing library.
"""

import argparse
import os
from samuel_regression_lib.db import MongoConnector
from samuel_regression_lib.xml_extractor import XMLExtractor


def add_reference_to_db(filepath, method):
    """
    Add a reference file to the database.

    Args:
        filepath (str): Path to the reference file
        method (str): Method name for the reference

    Returns:
        tuple: (success_status, message)
    """
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"

    # Extract data
    xml_data = XMLExtractor.extract_xml_from_file(filepath)
    output_data = XMLExtractor.extract_output_data(xml_data)

    if not output_data:
        return False, f"Could not extract output data from {filepath}"

    # Connect to database
    mongo = MongoConnector()
    connection_status, message = mongo.connect()

    if not connection_status:
        return False, f"Database connection failed: {message}"

    # Add to database
    filename = os.path.basename(filepath)
    success, message = mongo.add_reference(method, filename, xml_data, output_data)

    return success, message


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Regression Test CLI')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Add reference command
    add_parser = subparsers.add_parser('add-reference', help='Add a reference file to the database')
    add_parser.add_argument('filepath', help='Path to the reference file')
    add_parser.add_argument('method', help='Method name for the reference')

    args = parser.parse_args()

    if args.command == 'add-reference':
        success, message = add_reference_to_db(args.filepath, args.method)
        print(message)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()