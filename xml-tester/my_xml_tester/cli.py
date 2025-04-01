# my_xml_tester/cli.py
import argparse
from my_xml_tester.storage import store_xml

def main():
    parser = argparse.ArgumentParser(description="Save an XML file to storage.")
    parser.add_argument('xml_path', help="Path to the XML file to store")
    parser.add_argument('method_name', help="Method name under which to store the file")
    args = parser.parse_args()
    
    try:
        record = store_xml(args.xml_path, args.method_name)
        print(f"Stored record for {record['filename']}.")
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()
