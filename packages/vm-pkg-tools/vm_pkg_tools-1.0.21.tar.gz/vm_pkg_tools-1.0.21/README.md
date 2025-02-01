# README: vm-pkg-tools

## Overview

`vm-pkg-tools` is a Python package designed to facilitate parsing scout files for volleyball analytics. This document outlines the process to build, test, and deploy the package, as well as instructions to use it effectively.

---

## Directory Structure

Ensure the project structure aligns with the following:

```bash
project_root/
├── data/
│   └── scouts/
│       └── &1003.dvw
├── src/
│   ├── vm_pkg_tools/
│   │   ├── core/
│   │   │   ├── main.py
│   │   │   └── orchestrator.py
│   │   ├── parsers/
│   │   ├── utils/
│   │   └── validators/
├── tests/
├── README.md
├── requirements.txt
├── setup.py
└── dist/
```

---

## Requirements

### Runtime Dependencies

The following dependencies are required for the package to run:

- `click>=8.1,<9.0`
- `pydantic>=2.0,<3.0`
- `sqlalchemy>=2.0,<3.0`
- `PyYAML>=6.0,<7.0`
- `unidecode>=1.3,<2.0`
- `chardet>=5.0,<6.0`
- `colorlog>=6.0,<7.0`

### Development and Testing Dependencies

For local testing and development, include:

- `black>=24.10`
- `flake8>=7.1`
- `isort>=5.13`
- `pylint>=3.3`
- `pytest>=8.3.4`
- `attrs>=24.3`
- `twine`
- `setuptools`

---

## Installation

### Install Locally for Testing

1. Build the package:

   ```bash
   python setup.py sdist bdist_wheel
   ```

2. Install the package in a virtual environment:

   ```bash
   python -m venv test_env
   source test_env/bin/activate
   pip install dist/vm_pkg_tools-<version>-py3-none-any.whl
   ```

3. Verify installation:

   ```bash
   vmtools-cli --help
   ```

---

## Usage

### Parsing a Scout File

Ensure that the `data/scouts/` directory exists and contains the required scout file:

```bash
vmtools-cli parse data/scouts/&1003.dvw
```

---

## Testing the Package

1. Create a fresh virtual environment:

   ```bash
   python -m venv test_env
   source test_env/bin/activate
   ```

2. Install the built package:

   ```bash
   pip install dist/vm_pkg_tools-<version>-py3-none-any.whl
   ```

3. Run commands to verify functionality:

   ```bash
   vmtools-cli parse data/scouts/&1003.dvw
   ```

4. Run tests:

   ```bash
   pytest tests/
   ```

---

## Deployment

1. Remove old build artifacts:

   ```bash
   rm -rf build/ dist/ *.egg-info
   ```

2. Build the package:

   ```bash
   python setup.py sdist bdist_wheel
   ```

3. Upload to PyPI:

   ```bash
   twine upload dist/*
   ```

4. Verify the package on PyPI:
   [PyPI Project Page](https://pypi.org/project/vm-pkg-tools/)

---

## Versioning

### Tagging a Release

After testing and deploying, tag the release for version tracking:

```bash
git tag v<version>
git push origin v<version>
```

---

## Common Issues

### Missing Dependencies

If a dependency is missing during testing, add it to `install_requires` in `setup.py` and rebuild the package.

### File Not Found Errors

Ensure the required files are not ignored by `.gitignore` and exist in the expected directories.

### Import Errors

Verify all imports use the correct relative paths and update `PYTHONPATH` if necessary.

---

## License

This project is licensed under a **Custom Proprietary License**.

The use of this software is strictly prohibited for any of the following purposes without prior written consent from the author:

- Commercial use
- Redistribution or sublicensing
- Modification or derivation for other applications or platforms

By accessing this software, you agree to adhere to the terms outlined in the [LICENSE](LICENSE) file. For further details, see the [COPYRIGHT](COPYRIGHT) file.

For licensing inquiries, please contact the author:  
**Reza Barzegar Gashti**  
[rezabarzegargashti@gmail.com](mailto:rezabarzegargashti@gmail.com)
