# bamboogenerator

Python scripts for generating 3D printable models using the
`trimesh` library.  The repository contains a consolidated
`parametric_cad` package with example scripts that produce STL files.

## Folder layout

- **`parametric_cad/`** – library with primitives, mechanisms,
  STL export utilities and example scripts.

## Installation

Install the required Python packages and configure OpenSCAD using the
installer script in the repository root.  From the desired project directory run:

```bash
python install_requirements.py
```

This installs all Python dependencies and attempts to set up `trimesh` for OpenSCAD rendering.

## Running the examples

Set `PYTHONPATH` to the project directory and execute one of the scripts
from `parametric_cad/examples/`, for example:

```bash
export PYTHONPATH=.
python parametric_cad/examples/spur_gear_example.py
```
You can also run all examples at once using `run_examples.py` or the `run_examples.bat` script on Windows.

Generated STL files are written to `output/<example>_output/`.

## License

This project is licensed under the [MIT License](LICENSE).
