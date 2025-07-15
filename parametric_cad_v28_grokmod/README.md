Parametric CAD (Python-Based 3D Model Generator)
This project is a Python-based parametric CAD tool for generating 3D-printable .stl files programmatically. It supports creating basic shapes, mechanical components, and exporting them as STL files for 3D printing.
🧰 Requirements

Python 3.8+
Required libraries: trimesh, numpy, matplotlib, pyglet<2, networkx, scipy, shapely, triangle, mapbox_earcut, manifold3d, pillow

Install dependencies using the provided batch file (Windows):
install_requirements.bat

Or manually:
pip install trimesh numpy matplotlib "pyglet<2" networkx scipy shapely triangle mapbox_earcut manifold3d pillow

▶️ Running Examples (Windows)
Run all examples using the batch file:
example.bat

This generates STL files in the output folder:

output/box_with_door_output/box.stl
output/box_with_door_output/door_with_hinge.stl
output/hollow_box_output/hollow_box.stl
output/spur_gear_example_output/spur_gear.stl

💡 Manual Execution
Set the PYTHONPATH and run individual scripts:
cd parametric_cad
$env:PYTHONPATH = "."
python parametric_cad/examples/box_with_door.py
python parametric_cad/examples/hollow_box.py
python parametric_cad/examples/spur_gear_example.py

📦 Folder Structure

parametric_cad/primitives: Basic shapes (Box, SpurGear)
parametric_cad/mechanisms: Mechanical parts (ButtHinge)
parametric_cad/export: STL export functionality (stl.py)
examples/: Example scripts generating printable parts
output/: Generated STL files and preview images

📄 Example Outputs

Box with Door: A box (100x60x40mm) with a hinged door (100x3x40mm) and a hinge pin.
Hollow Box: A box (100x60x40mm) with a hollowed interior (90x50x30mm).
Spur Gear: A gear with 20 teeth, module 1.0, 8mm width, 5mm bore, and 6 screw holes.

🚀 Future Ideas

Add more shapes (cylinders, spheres, bevel gears)
Implement constraints (align, attach, snap-to)
Expand part libraries (fan ducts, brackets, mounts)
Add support for threaded holes and fasteners
Improve preview rendering with customizable angles

⚠️ Notes

Ensure all dependencies are installed before running examples.
Generated STL files are saved in the output subfolder corresponding to each example.
Preview images (PNG) are generated for each STL file if pyglet and pillow are installed.
