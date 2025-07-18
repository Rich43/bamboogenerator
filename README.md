# bamboogenerator

Python scripts for generating 3D printable models.  The project now
leverages the [CadQuery](https://github.com/CadQuery/cadquery)
library for creating geometry while still providing utilities for
scaffolding generation and printability validation. The repository
contains a consolidated `parametric_cad` package with example scripts
that produce STL files.

## Folder layout

- **`parametric_cad/`** – library with primitives, mechanisms,
  STL export utilities and example scripts.

## Installation

Install the required Python packages and configure OpenSCAD using the
installer script in the repository root.  From the desired project directory run:

```bash
python install_requirements.py
```

This installs all Python dependencies including CadQuery. It also
configures `trimesh` for OpenSCAD rendering which is still used under
the hood for mesh operations.

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

### Using CadQuery

CadQuery models can also be used with the validation and scaffolding
utilities by converting a `Workplane` to a `trimesh` mesh:

```python
import cadquery as cq
from parametric_cad import workplane_to_mesh, generate_scaffolding

wp = cq.Workplane("XY").box(10, 10, 5)
mesh = workplane_to_mesh(wp)
supports = generate_scaffolding(mesh)
```

You can also operate on CadQuery models directly using helper wrappers:

```python
import cadquery as cq
from parametric_cad import generate_scaffolding_from_workplane, PrintabilityValidator

wp = cq.Workplane("XY").box(10, 10, 5)
supports = generate_scaffolding_from_workplane(wp)
errors = PrintabilityValidator().validate_workplane(wp)
```

## Overhang Scaffolding

`generate_scaffolding` creates simple cylindrical supports beneath
downward facing surfaces that exceed a chosen overhang angle.  The supports
are meant to be easy to remove after printing.

```python
from parametric_cad import generate_scaffolding, Box, combine

base = Box(20, 20, 10)
ledge = Box(10, 10, 5).at(15, 5, 10)
model = combine([base, ledge])
supports = generate_scaffolding(model)
```

## License

This project is licensed under the [MIT License](LICENSE).
