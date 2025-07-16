# bamboogenerator

Python scripts for generating 3D printable models using the
`trimesh` library.  The repository contains two related parametric CAD
implementations along with example scripts that produce STL files.

## Folder layout

- **`3d_model_maker/`** – simple parametric CAD package with
  primitives, basic mechanisms and a `run_example.py` helper.
- **`parametric_cad_v28_grokmod/`** – a more feature rich variant of
  the library containing the same core modules and additional example
  scripts.
- Each of these folders contains a `parametric_cad/` package with
  sub‑directories:
  - `primitives/` – basic shapes such as `Box` and `Gear`.
  - `mechanisms/` – mechanical components like hinges.
  - `export/` – STL export helpers.
  - `examples/` – small scripts demonstrating library usage.

## Installation

Install the required Python packages and configure OpenSCAD using the
provided installer script.  From the desired project directory run:

```bash
python install_requirements.py
```

This installs all Python dependencies and attempts to set up
`trimesh` for OpenSCAD rendering.  Each top‑level project folder has
its own copy of this script.

## Running the examples

The `run_example.py` script in `3d_model_maker/` automatically runs the
example scripts and places results in the `output/` folder:

```bash
cd 3d_model_maker
python run_example.py
```

To run an individual example manually, set `PYTHONPATH` to the
`parametric_cad` package and execute one of the scripts from the
`examples/` directory, e.g.:

```bash
cd parametric_cad_v28_grokmod
export PYTHONPATH=.
python parametric_cad/examples/spur_gear_example.py
```

Generated STL files are written to `output/<example>_output/`.

## License

This project is licensed under the [MIT License](LICENSE).
