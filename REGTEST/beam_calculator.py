#!/usr/bin/env python3
"""
Beam Calculator with Regression Testing

This script demonstrates how to use the regression testing library with a beam calculation application.
"""

import os
import sys
import argparse
import xml.etree.ElementTree as ET
import math
from samuel_regression_lib import RegressionTest

# Dictionary mapping method shortcuts to full method names
METHOD_MAPPING = {
    "lq": "lineSquareTube",
    "cr": "circularRound",
    "cb": "circularBeam"
}


def calculate_beam_properties(xml_file, method):
    """
    Calculate beam properties based on the input XML and method.

    Args:
        xml_file (str): Path to the XML file
        method (str): Calculation method to use

    Returns:
        dict: Calculated output properties
    """
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract input data
    material = root.find('.//MATERIAL')
    dimensions = root.find('.//DIMENSIONS')
    load = root.find('.//LOAD')

    # Extract material properties
    material_type = material.find('TYPE').text
    strength = float(material.find('STRENGTH').text)
    density = float(material.find('DENSITY').text)
    elasticity = float(material.find('ELASTICITY').text)

    # Extract dimensions
    length = float(dimensions.find('LENGTH').text)
    width = float(dimensions.find('WIDTH').text)
    height = float(dimensions.find('HEIGHT').text)
    thickness = float(dimensions.find('THICKNESS').text)

    # Extract load information
    distributed_load = float(load.find('DISTRIBUTED').text)
    point_load = float(load.find('POINT_LOAD').text)
    point_position = float(load.find('POINT_POSITION').text)

    # Calculate different properties based on the method
    if method == "lineSquareTube":
        # Square tube calculations
        outer_area = width * height
        inner_area = (width - 2 * thickness) * (height - 2 * thickness)
        area = outer_area - inner_area

        # Calculate section modulus
        outer_inertia = (width * height ** 3) / 12
        inner_inertia = ((width - 2 * thickness) * (height - 2 * thickness) ** 3) / 12
        moment_of_inertia = outer_inertia - inner_inertia
        section_modulus = moment_of_inertia / (height / 2)

        # Calculate stress (simplified beam equation)
        moment = (distributed_load * length ** 2 / 8) + (point_load * point_position / 2)
        max_stress = moment / section_modulus

        # Calculate deflection (simplified)
        deflection_factor = 5 if distributed_load > point_load else 1
        max_deflection = (deflection_factor * distributed_load * length ** 4) / (384 * elasticity * moment_of_inertia)
        max_deflection += (point_load * length ** 3) / (48 * elasticity * moment_of_inertia)

        # Calculate weight
        volume = area * length / 1000  # Convert to m^3
        weight = volume * density / 1000  # Convert to kg

        # Calculate safety factor
        safety_factor = strength / max_stress

    elif method == "circularRound":
        # Circular beam calculations
        radius = width / 2
        area = math.pi * radius ** 2

        # Calculate section modulus
        moment_of_inertia = (math.pi * radius ** 4) / 4
        section_modulus = moment_of_inertia / radius

        # Calculate stress
        moment = (distributed_load * length ** 2 / 8) + (point_load * point_position / 2)
        max_stress = moment / section_modulus

        # Calculate deflection
        deflection_factor = 5 if distributed_load > point_load else 1
        max_deflection = (deflection_factor * distributed_load * length ** 4) / (384 * elasticity * moment_of_inertia)
        max_deflection += (point_load * length ** 3) / (48 * elasticity * moment_of_inertia)

        # Calculate weight
        volume = area * length / 1000  # Convert to m^3
        weight = volume * density / 1000  # Convert to kg

        # Calculate safety factor
        safety_factor = strength / max_stress

    elif method == "circularBeam":
        # Circular beam with hollow core
        outer_radius = width / 2
        inner_radius = outer_radius - thickness
        area = math.pi * (outer_radius ** 2 - inner_radius ** 2)

        # Calculate section modulus
        outer_inertia = (math.pi * outer_radius ** 4) / 4
        inner_inertia = (math.pi * inner_radius ** 4) / 4
        moment_of_inertia = outer_inertia - inner_inertia
        section_modulus = moment_of_inertia / outer_radius

        # Calculate stress
        moment = (distributed_load * length ** 2 / 8) + (point_load * point_position / 2)
        max_stress = moment / section_modulus

        # Calculate deflection
        deflection_factor = 5 if distributed_load > point_load else 1
        max_deflection = (deflection_factor * distributed_load * length ** 4) / (384 * elasticity * moment_of_inertia)
        max_deflection += (point_load * length ** 3) / (48 * elasticity * moment_of_inertia)

        # Calculate weight
        volume = area * length / 1000  # Convert to m^3
        weight = volume * density / 1000  # Convert to kg

        # Calculate safety factor
        safety_factor = strength / max_stress

    else:
        raise ValueError(f"Unknown method: {method}")

    # Round values for cleaner output
    max_stress = round(max_stress, 2)
    max_deflection = round(max_deflection, 2)
    section_modulus = round(section_modulus, 2)
    moment_of_inertia = round(moment_of_inertia, 2)
    weight = round(weight, 2)
    safety_factor = round(safety_factor, 2)

    # Create output dictionary
    output = {
        "MAX_STRESS": max_stress,
        "MAX_DEFLECTION": max_deflection,
        "SECTION_MODULUS": section_modulus,
        "MOMENT_OF_INERTIA": moment_of_inertia,
        "TOTAL_WEIGHT": weight,
        "SAFETY_FACTOR": safety_factor
    }

    return output


def get_reference_output(xml_file):
    """
    Extract reference output from the XML file.

    Args:
        xml_file (str): Path to the XML file

    Returns:
        dict: Reference output data
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # In our sample, the output tag is named 'o'
    output_elem = root.find(".//o")

    if output_elem is None:
        return None

    # Extract output values
    output = {}
    for child in output_elem:
        tag = child.tag
        try:
            # Try to convert to float if possible
            value = float(child.text)
        except (ValueError, TypeError):
            value = child.text

        output[tag] = value

    return output


def main():
    """Main function for the beam calculator."""
    parser = argparse.ArgumentParser(description='Beam Calculator with Regression Testing')
    parser.add_argument('method', choices=METHOD_MAPPING.keys(), help='Calculation method')
    parser.add_argument('--files', nargs='+', help='XML files to process')
    parser.add_argument('--dir', help='Directory containing XML files to process')
    parser.add_argument('--test', action='store_true', help='Run regression tests')
    parser.add_argument('--add-reference', action='store_true',
                        help='Add processed files as references to the database')

    args = parser.parse_args()

    # Determine which files to process
    files_to_process = []
    if args.files:
        files_to_process = args.files
    elif args.dir:
        if not os.path.isdir(args.dir):
            print(f"Error: Directory not found: {args.dir}")
            return 1
        files_to_process = [os.path.join(args.dir, f) for f in os.listdir(args.dir)
                            if f.endswith('.xml')]
    else:
        parser.print_help()
        return 1

    # Get the full method name
    method = METHOD_MAPPING[args.method]

    # Initialize regression test if needed
    if args.test or args.add_reference:
        from samuel_regression_lib import RegressionTest, add_reference_to_db

    if args.test:
        regression = RegressionTest()

    # Process each file
    results = {}
    for xml_file in files_to_process:
        try:
            # Check if the file exists
            if not os.path.isfile(xml_file):
                print(f"Error: File not found: {xml_file}")
                continue

            # Get the base filename
            basename = os.path.basename(xml_file)

            # Calculate the beam properties
            output = calculate_beam_properties(xml_file, method)
            results[basename] = output

            # Print the results
            print(f"\nResults for {basename} using method {method}:")
            for key, value in output.items():
                print(f"{key}: {value}")

            # Perform regression testing if requested
            if args.test:
                print(f"\nRunning regression test for {basename}...")
                test_status = regression.test_file(basename, method, output)
                print(f"Test status: {test_status}")

            # Add reference to database if requested
            if args.add_reference:
                print(f"\nAdding {basename} as reference for method {method}...")
                from regression_test.cli import add_reference_to_db
                success, message = add_reference_to_db(xml_file, method)
                print(message)

        except Exception as e:
            print(f"Error processing {xml_file}: {str(e)}")

    # Print regression test results
    if args.test:
        print("\nRegression Test Results:")
        print(regression.get_results())

    return 0


if __name__ == "__main__":
    sys.exit(main())