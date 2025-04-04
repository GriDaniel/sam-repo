import sys
import argparse
from pathlib import Path

# Add the parent directory (project root) to sys.path
sys.path.append(str(Path(__file__).parent.parent))

# Now you can import from core
from core.db import get_db_connection, store_document
from core.extractor import extract_metadata_from_xml
from core.xml_to_json import xml_to_json


def add_file_to_db(file_path: Path, method_name: str, verbose: bool = False) -> bool:
    """Add an XML file to the database with the full filename, including the .xml extension."""
    if not file_path.is_file() or file_path.suffix.lower() != '.xml':
        print(f"Error: '{file_path}' is not a valid XML file")
        return False

    db, db_result = get_db_connection()
    if verbose:
        print(db_result)
    if db is None:
        print("Database connection failed")
        return False

    try:
        metadata, extract_result = extract_metadata_from_xml(file_path)
        json_data, json_result = xml_to_json(file_path)
        if verbose:
            print(extract_result, json_result)

        # Store the document with the full filename (including .xml extension)
        store_result = store_document(db, method_name, file_path.name, json_data, metadata)
        if verbose:
            print(store_result)

        print(f"File '{file_path.name}' added to database under method '{method_name}'")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def process_directory(directory: Path, method_name: str, verbose: bool):
    """Process all XML files in a directory."""
    success, failed = 0, 0
    for file_path in directory.glob("*.xml"):
        print(f"Processing {file_path.name}...")
        if add_file_to_db(file_path, method_name, verbose):
            success += 1
        else:
            failed += 1
    print(f"Batch complete: {success} added, {failed} failed")

def main():
    parser = argparse.ArgumentParser(description="Add XML files to the SAM Registry database")
    parser.add_argument("file_path", type=Path, help="Path to the XML file or directory")
    parser.add_argument("method_name", help="Method name for storage")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable detailed output")
    parser.add_argument("-b", "--batch", action="store_true", help="Process all XML files in a directory")

    args = parser.parse_args()

    if args.file_path.is_dir() and args.batch:
        process_directory(args.file_path, args.method_name, args.verbose)
    elif add_file_to_db(args.file_path, args.method_name, args.verbose):
        print("File added successfully")
    else:
        print("Failed to add file")
        sys.exit(1)

if __name__ == "__main__":
    main()
