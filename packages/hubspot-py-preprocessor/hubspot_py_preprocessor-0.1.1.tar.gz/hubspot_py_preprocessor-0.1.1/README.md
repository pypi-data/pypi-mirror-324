# Python Import Extractor and Code Processor

This Python script is designed to address a specific challenge when working with **custom code in HubSpot workflows**. HubSpot does not allow the use of custom libraries or imports in its workflows, forcing developers to duplicate code across multiple workflows. This script helps streamline this process by extracting and organizing reusable code snippets, making it easier to manage and maintain custom logic across workflows.

Beyond being a simple library, this project proposes a **development and code organization strategy** tailored for HubSpot workflows. It ensures modularity, reusability, and maintainability by structuring code into specific directories and enforcing import conventions.

---

## Features

- **Import Extraction**: Recursively extracts imports and reusable functions from Python files, including nested imports.
- **Code Classification**: Classifies code into standard libraries, constants, and custom libraries for better organization.
- **Code Deduplication**: Helps avoid code duplication by extracting reusable functions and constants into a centralized structure.
- **HubSpot Workflow Compatibility**: Generates clean, self-contained code snippets that can be directly used in HubSpot workflows.
- **Development Organization**: Provides a clear directory structure and import conventions for scalable development.
- **Path Handling**: Uses `pathlib` and `os` for cross-platform file and directory management.
- **Logging**: Provides detailed logging for debugging and tracking operations.
- **Customizable Depth**: Allows setting a maximum depth for recursive import analysis.

---

## Why This Script?

When working with **HubSpot workflows**, developers often face the limitation of not being able to import custom libraries or shared code. This leads to:

- **Code Duplication**: The same functions or constants are copied across multiple workflows, making maintenance difficult.
- **Error-Prone Updates**: Changes to shared logic require manual updates in every workflow, increasing the risk of inconsistencies.
- **Lack of Modularity**: Without the ability to import libraries, workflows become cluttered and harder to manage.

This script solves these issues by:

1. Extracting reusable code (functions, constants, etc.) from your custom libraries.
2. Organizing the extracted code into a structured format.
3. Generating clean, self-contained code snippets that can be directly used in HubSpot workflows.

---

## Development Organization

The code is organized into the following directories:

```
project-root/
│
├── customcode/ # Main programs to be analyzed
│ ├── workflow1.py
│ ├── workflow2.py
│ └── ...
│
├── lib/ # Custom function libraries
│ ├── utils.py
│ ├── helpers.py
│ └── ...
│
├── constants/ # HubSpot environment constants
│ ├── pipelines.py # Example: Pipeline IDs and names
│ ├── stages.py # Example: Stage IDs and names
│ ├── properties.py # Example: Custom property names
│ └── ...
│
└── generated/ # Results of transformations
├── workflow1.py
├── workflow2.py
└── ...
```

### Directory Roles

- **`customcode/`**: Contains the main programs (e.g., HubSpot workflows) that will be analyzed. These files are the entry points for the script.
- **`lib/`**: Stores reusable functions and utilities. These are shared across multiple workflows to avoid duplication.
- **`constants/`**: Contains environment-specific constants, such as HubSpot pipeline IDs, stage IDs, or custom property names. These are centralized to ensure consistency.
- **`generated/`**: Stores the output files after processing. These files are self-contained and ready to be used in HubSpot workflows.

---

## Import Conventions

To ensure clean and modular code, the following import conventions are enforced:

1. **Use `from ... import`**:
  
  - Always use `from mylib import function_name` instead of `import mylib`.
  - This avoids the need to prefix function calls with `mylib.function_name()`, making the code cleaner and more readable.
  
  **Example**:
  
  ```python
  # Good
  from lib.utils import format_date, calculate_discount
  
  # Bad
  import lib.utils
  ```
  
2. **Avoid Package References**:
  

By using `from ... import`, you ensure that the generated code does not rely on package structures.

3. **Centralize Constants**:

Import constants from the constants/ directory to ensure consistency across workflows.

4. **Examples**:
  
  ```python
  from constants.pipelines import SALES_PIPELINE_ID
  from constants.stages import QUALIFIED_LEAD_STAGE_ID
  ```
  

# Command Line Usage (CLI)

The program can be used via the hsprocessor command (defined by hubspot_py_preprocessor.cli:main).

# Installation

```bash
pip install hubspot-py-preprocessor
```

# Usage

```bash
hsprocessor /path/to/your/code /path/to/output/dir --max_depth 5
```

- **`customcode/`**: Contains the main programs (e.g., HubSpot workflows) that will be analyzed. These files are the entry points for the script.

- **`/path/to/your/project`** (required): The root directory where your Python files are located. The script will recursively scan all .py files in this folder.

- **`/path/to/output/dir`** (required): The directory where the processed (inlined) Python files will be saved.

- **`--max_depth 5`** (optional): Sets the maximum recursion depth for analyzing imports. By default, it is 10.

If you omit the --max_depth parameter, the script defaults to 10. Here’s a summary of the main arguments:



- **`input_directory`** ( **`str`**): The path to the project folder containing your Python files.
- **`output_directory (**`str`**): The path to the folder where processed files should be saved.
- **`--max_depth`** ( **`int`**, default= **`10`**): Specifies how many levels of nested imports to analyze before stopping.

When you run the command, the script will:

1. Recursively traverse the specified input_directory.
2. Identify and inline any custom imports within each Python file according to the rules set by the preprocessor.
3. Generate new self-contained Python files in the output_directory.

Use the **`--help`** flag to see a quick reference of all available arguments.

## License

MIT License

Copyright (c) [2005] [David BRAHIM]

---

## Contact

Open an issue to get help or suggest improvements.