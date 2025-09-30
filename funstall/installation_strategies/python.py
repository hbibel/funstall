def update(pypi_package_name: str) -> None:
    pass

    # Check if Python version is still supported; if not, recreate venv
    # Here's a fun little document to read for this
    # https://packaging.python.org/en/latest/specifications/version-specifiers/#id5

    # pip metadata for checking Python version: https://pypi.org/pypi/<package name>/json
    # https://pypi.org/pypi/funstall/json
    # -> key info.requires_python

    # pip install <package_name> --upgrade
