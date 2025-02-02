import argparse
from hubspot_py_preprocessor.inliner import process_directory,logger

def main():
    parser = argparse.ArgumentParser(description="Process a directory of Python files and extract imports.")
    parser.add_argument('input_directory', type=str, help='The root directory to scan for Python files.')
    parser.add_argument('output_directory', type=str, help='The directory where processed files will be saved.')
    parser.add_argument('--max_depth', type=int, default=10, help='The maximum depth for analyzing imports in each file (default: 10).')

    args = parser.parse_args()

    try:
        process_directory(
            input_directory=args.input_directory,
            output_directory=args.output_directory,
            max_depth=args.max_depth
        )
    except FileNotFoundError as e:
        logger.error(e)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()