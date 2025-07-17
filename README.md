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
You can also run all examples at once using the cross-platform `run_examples.py` script.

Generated STL files are written to `output/<example>_output/`.

## Combining Primitives

Functions `combine` and `safe_difference` from
[`parametric_cad/core.py`](parametric_cad/core.py) help manipulate meshes.

- **`combine(objects)`** – returns the union of the provided meshes or
  primitives by concatenating their geometry.
- **`safe_difference(mesh, other)`** – subtracts one mesh (or list of meshes)
  from another and gracefully falls back to the original mesh if the boolean
  operation fails.

Example:

```python
from parametric_cad.primitives import Box, Cylinder
from parametric_cad.core import combine, safe_difference

boxes = [Box(1, 1, 1).at(x, 0, 0) for x in range(3)]
unioned = combine(boxes)
result = safe_difference(unioned, Cylinder(0.5, 1).mesh())
```

## License

This project is licensed under the [MIT License](LICENSE).
