import os
import json
import logging
import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from vm_pkg_tools.core.orchestrator import parse_dvw_file
from vm_pkg_tools.utils.file_utils import read_scout_file
from vm_pkg_tools.utils.logger import setup_logging

# Configure logging with appropriate levels for console and file
setup_logging(console_level=logging.INFO, file_level=logging.DEBUG)


def ensure_directory_exists(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)


def main(input_file=None, output_file=None):
    """
    Main entry point for parsing scout files.
    """
    input_file = input_file or os.path.join("data", "scouts", "&1003.dvw")
    output_file = output_file or os.path.join(
        "output", "json", "full_parsed_output.json"
    )

    try:
        logging.info(f"Starting scout file parsing: {input_file}")
        scout_content = read_scout_file(input_file)
        parsed_data = parse_dvw_file(scout_content)

        ensure_directory_exists(output_file)
        with open(output_file, "w", encoding="utf-8") as output_file:
            json.dump(parsed_data, output_file, ensure_ascii=False, indent=4)

        logging.info(f"Successfully wrote the output to: {output_file.name}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a DVW scout file.")
    parser.add_argument(
        "--input_file",
        type=str,
        help="Path to the input scout file.",
        required=False,
    )
    parser.add_argument(
        "--output_file",
        type=str,
        help="Path to save the parsed output.",
        required=False,
    )
    args = parser.parse_args()
    main(input_file=args.input_file, output_file=args.output_file)
