import ast
import os
import re
import argparse
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def is_lib_or_constants(name: str):
    """
    Returns True if the module name starts with 'lib' or 'constants'
    (e.g., 'lib', 'lib.sub', 'constants', 'constants.sub').
    """
    if not name:
        return False
    return (
        name == "lib"
        or name.startswith("lib.")
        or name == "constants"
        or name.startswith("constants.")
    )


def package_to_path(package_name: str):
    """
    Converts a package name (e.g., 'lib.utils') into a file path
    (e.g., 'lib/utils.py').
    """
    return package_name.replace(".", os.sep) + ".py"


def get_symbol_code(file_path: str, symbol_name: str, alias_name: str = None):
    """
    Opens the Python file 'file_path' and searches for a function/assignment
    named 'symbol_name'. If found, extracts the corresponding snippet.

    - If 'alias_name' is not None, renames the declaration line to reflect the alias.
    - Otherwise, returns the snippet as is.
    - Returns None if not found or if the file does not exist.
    """
    if not os.path.isfile(path=file_path):
        return None

    with open(file=file_path, mode="r", encoding="utf-8") as f:
        lines = f.readlines()

    try:
        tree = ast.parse(source="".join(lines), filename=file_path)
    except SyntaxError:
        return None

    for node in ast.walk(node=tree):
        # Cas fonction 'def symbol_name(...)'
        if isinstance(node, ast.FunctionDef) and node.name == symbol_name:
            start = node.lineno - 1
            end = getattr(node, "end_lineno", None)
            if end is None:
                continue
            snippet = "".join(lines[start:end])
            if alias_name:
                snippet = rename_in_code_snippet(
                    original_snippet=snippet,
                    node=node,
                    original_name=symbol_name,
                    alias_name=alias_name,
                )
            return snippet.rstrip("\n")

        # Cas assignation 'symbol_name = ...'
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == symbol_name
        ):
            start = node.lineno - 1
            end = getattr(node, "end_lineno", None)
            if end is None:
                continue
            snippet = "".join(lines[start:end])
            if alias_name:
                snippet = rename_in_code_snippet(
                    original_snippet=snippet,
                    node=node,
                    original_name=symbol_name,
                    alias_name=alias_name,
                )
            return snippet.rstrip("\n")

    return None


def rename_in_code_snippet(original_snippet, node, original_name, alias_name):
    """
    Renames 'original_name' to 'alias_name' in the function/assignment source code.
    """
    if not alias_name:
        return original_snippet

    lines = original_snippet.splitlines(True)

    if isinstance(node, ast.FunctionDef):
        pattern = r"^(async\s+)?def\s+" + re.escape(original_name) + r"(\s*\()"
        replace = r"\1def " + alias_name + r"\2"
        for i, line in enumerate(lines):
            new_line = re.sub(pattern=pattern, repl=replace, string=line)
            if new_line != line:
                lines[i] = new_line
                break

    elif isinstance(node, ast.Assign):
        pattern = r"^(\s*)" + re.escape(original_name) + r"(\s*=\s*)"
        replace = r"\1" + alias_name + r"\2"
        for i, line in enumerate(lines):
            new_line = re.sub(pattern=pattern, repl=replace, string=line)
            if new_line != line:
                lines[i] = new_line
                break

    return "".join(lines)


def extract_imports_as_dicts(
    filepath: str, imports_list, visited=None, depth=0, max_depth=10
):
    """
    Recursively extracts imports from a Python file, up to a maximum depth.
    """
    if not os.path.isfile(path=filepath) or depth > max_depth:
        return imports_list

    if visited is None:
        visited = set()

    if filepath in visited:
        return imports_list

    visited.add(filepath)

    with open(file=filepath, mode="r", encoding="utf-8") as f:
        lines = f.readlines()

    try:
        tree = ast.parse(source="".join(lines), filename=filepath)
    except SyntaxError:
        return imports_list

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_code = "".join(
                lines[node.lineno - 1 : getattr(node, "end_lineno", node.lineno)]
            )
            for alias in node.names:
                module_name = alias.name
                module_path = package_to_path(package_name=module_name)
                dct_import = {
                    "package": module_name,
                    "module": None,
                    "alias": alias.asname,
                    "code": import_code,
                    "depth": depth,
                }
                imports_list.append(dct_import)

                if os.path.isfile(path=module_path):
                    extract_imports_as_dicts(
                        filepath=module_path,
                        imports_list=imports_list,
                        visited=visited,
                        depth=depth + 1,
                        max_depth=max_depth,
                    )

        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue

            import_code = "".join(
                lines[node.lineno - 1 : getattr(node, "end_lineno", node.lineno)]
            )
            module_path = package_to_path(package_name=node.module)

            for alias in node.names:
                symbol_code = None

                if is_lib_or_constants(node.module):
                    symbol_code = get_symbol_code(
                        file_path=module_path,
                        symbol_name=alias.name,
                        alias_name=alias.asname,
                    )

                dct_import = {
                    "package": node.module,
                    "module": alias.name,
                    "alias": alias.asname,
                    "code": symbol_code or import_code,
                    "depth": depth,
                }
                imports_list.append(dct_import)

                if os.path.isfile(path=module_path):
                    extract_imports_as_dicts(
                        filepath=module_path,
                        imports_list=imports_list,
                        visited=visited,
                        depth=depth + 1,
                        max_depth=max_depth,
                    )
    return imports_list


def extract_libs_from_dict(
    libraries: dict,
    filter: str = None,
    exclude_prefixes: tuple = ("lib.", "constants."),
):
    """
    Filters and retrieves imports from a given dictionary.

    - If a filter is provided, retrieves only libraries that start with the filter string.
    - If no filter is provided, excludes libraries starting with 'lib.' or 'constants.' by default.
    - Ensures that duplicate imports are not included.
    """
    seen = set()
    filtered_data = []
    for item in libraries:
        if (
            (filter and item["package"].startswith(filter))
            or (not filter and not item["package"].startswith(exclude_prefixes))
        ) and item["code"] not in seen:
            filtered_data.append(item["code"])
            seen.add(item["code"])
    return filtered_data


def replace_directory_with_pathlib(file_path: str, old_dir: str, new_dir: str):
    """
    Replaces 'old_dir' with 'new_dir' in the given file path using pathlib.

    - If 'old_dir' is found in the path, it is replaced.
    - If 'old_dir' is not found, the path remains unchanged.
    """
    path = Path(file_path)
    parts = list(path.parts)  # Divise le chemin en ses composantes
    # Remplace le répertoire si l'ancien est trouvé
    try:
        index = parts.index(old_dir)
        parts[index] = new_dir
    except ValueError:
        pass  # Si l'ancien répertoire n'est pas trouvé, ne rien faire
    return Path(*parts)


def remove_imports_from_file(file_path: str):
    """
    Supprime toutes les lignes d'importation dans un fichier source Python (y compris les imports multi-lignes avec des parenthèses)
    et retourne le reste du code.

    Args:
        file_path (str): Chemin du fichier source Python.

    Returns:
        str: Code du fichier sans les lignes d'importation.
    """
    with open(file=file_path, mode="r") as file:
        code_lines = file.readlines()

    filtered_code = []
    inside_import_block = False

    for line in code_lines:
        stripped_line = line.strip()

        # Détecter le début d'un import (supporte les parenthèses)
        if re.match(r"^\s*(import|from\s+\S+\s+import)", stripped_line):
            inside_import_block = True

        # Vérifier si c'est la fin d'un bloc d'import multi-ligne
        if inside_import_block:
            if stripped_line.endswith(")"):  # Fin de bloc
                inside_import_block = False
            continue  # Ignorer les lignes d'import

        # Ajouter les autres lignes (non-import)
        filtered_code.append(line)

    return "".join(filtered_code)


def write_output_file(
    file_path: str, std_libs: list, constante_libs: list, code_libs: list, source: str
):
    with open(file=file_path, mode="w") as file:
        file.write("# Generated file : DON'T UPDATE\n")
        for lib in std_libs:
            file.write(lib)
        file.write("# CONSTANTE\n")
        for lib in constante_libs:
            file.write(lib + "\n")
        file.write("# FUNCTION\n")
        for lib in code_libs:
            file.write("\n" + lib + "\n")
        file.write("# SOURCE CODE\n")
        file.write(source)


import os


def process_file(input_path: str, output_directory: str, max_depth: int = 10):
    """
    Processes a Python file by extracting its imports, classifying them,
    and writing the modified content to an output file.

    This function:
    - Checks if the input file exists.
    - Extracts and categorizes imports from the file.
    - Removes imports from the source code.
    - Saves the modified source code along with categorized imports in the output directory.

    :param input_path: The full path of the input Python file to process.
    :param output_directory: The directory where the processed file will be saved.
    :param max_depth: The maximum depth for analyzing imports in the file (default: 10).

    :raises FileNotFoundError: If the specified input file does not exist.

    :example usage:
        process_file("scripts/example.py", "processed_scripts")
    """
    # Check if the input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The file {input_path} does not exist.")

    # Extract the filename from the path
    file_name = os.path.basename(input_path)

    # Construct the output file path
    output_path = os.path.join(output_directory, file_name)

    my_imports = []
    imported_libraries = extract_imports_as_dicts(
        filepath=input_path, imports_list=my_imports, max_depth=max_depth
    )
    # Ensure the output directory exists, create it if necessary
    os.makedirs(output_directory, exist_ok=True)

    write_output_file(
        file_path=output_path,
        std_libs=extract_libs_from_dict(imported_libraries),
        constante_libs=extract_libs_from_dict(imported_libraries, "constants."),
        code_libs=extract_libs_from_dict(imported_libraries, "lib."),
        source=remove_imports_from_file(input_path),
    )

def process_directory(input_directory: str, output_directory: str, max_depth: int = 10):
    """
    Recursively traverses an input directory, finds all Python (.py) files,
    and processes each one using `process_file`.

    The processed files are saved in the specified output directory,
    maintaining the original directory structure.

    :param input_directory: The root directory to scan for Python files.
    :param output_directory: The directory where processed files will be saved.
    :param max_depth: The maximum depth for analyzing imports in each file (default: 10).

    :raises FileNotFoundError: If the specified input directory does not exist.
    """

    # Check if the input directory exists
    if not os.path.exists(input_directory):
        raise FileNotFoundError(f"The directory {input_directory} does not exist.")

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Walk through the input directory recursively
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".py"):  # Process only Python files
                input_file_path = os.path.join(root, file)

                # Compute the corresponding output file path
                relative_path = os.path.relpath(input_file_path, input_directory)
                output_file_path = os.path.join(output_directory, relative_path)

                # Ensure the directory structure is replicated in the output directory
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                logger.info(f"Processing: {input_file_path} -> {output_file_path}")
                process_file(
                    input_path=input_file_path,
                    output_directory=os.path.dirname(output_file_path),
                    max_depth=max_depth,
                )

    logger.info(
        f"All Python files have been processed and saved in: {output_directory}"
    )

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
