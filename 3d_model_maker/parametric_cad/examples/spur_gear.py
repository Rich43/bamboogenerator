import trimesh
from parametric_cad.primitives.spurgear import SpurGear
from parametric_cad.export.stl import STLExporter

def create_spur_gear_example(teeth=20, module=2.0, thickness=10.0, pressure_angle=20.0):
    """
    Create a spur gear example with specified parameters.
    
    Args:
        teeth (int): Number of teeth (default: 20)
        module (float): Module (pitch diameter / number of teeth, default: 2.0 mm)
        thickness (float): Thickness of the gear (default: 10.0 mm)
        pressure_angle (float): Pressure angle in degrees (default: 20.0)
    
    Returns:
        trimesh.Trimesh: Gear mesh
    """
    # Create the spur gear
    gear = SpurGear(teeth=teeth, module=module, thickness=thickness, pressure_angle=pressure_angle)
    return gear.mesh

if __name__ == "__main__":
    # Example usage with multiple gear variations
    exporter = STLExporter(output_dir="output/spur_gear_example_output")

    # Create and export a default gear
    default_gear_mesh = create_spur_gear_example()
    exporter.export_mesh(default_gear_mesh, "spur_gear_default")

    # Create and export a larger gear with more teeth
    large_gear_mesh = create_spur_gear_example(teeth=30, module=3.0, thickness=15.0)
    exporter.export_mesh(large_gear_mesh, "spur_gear_large")

    print("Spur gear examples exported to output/spur_gear_example_output/")
    