import numpy as np
import trimesh
from shapely.geometry import Polygon
from math import pi, sin, cos, tan
import logging

# Set up logging to file
logging.basicConfig(filename='gear_debug.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class SpurGear:
    def __init__(self, module, teeth, width=5.0, bore_diameter=5.0, hole_count=0, hole_diameter=2.0, hole_radius=None):
        self.module = module
        self.teeth = teeth
        self.width = width
        self.bore_diameter = bore_diameter
        self.hole_count = hole_count
        self.hole_diameter = hole_diameter
        self.hole_radius = hole_radius or (self.pitch_diameter / 2 + module * 1.5)
        logging.debug(f"Initialized SpurGear: module={module}, teeth={teeth}, width={width}, bore={bore_diameter}, holes={hole_count}")

    @property
    def pitch_diameter(self):
        return self.module * self.teeth

    @property
    def base_diameter(self):
        pressure_angle = 20 * pi / 180
        return self.pitch_diameter * cos(pressure_angle)

    @property
    def addendum(self):
        return self.module

    @property
    def dedendum(self):
        return 1.25 * self.module

    def involute_profile(self, base_radius, outer_radius, steps=10):
        theta = np.linspace(0, np.arccos(base_radius / outer_radius), steps)
        x = base_radius * (np.cos(theta) + theta * np.tan(theta))
        y = base_radius * (np.sin(theta) - theta * np.tan(theta))
        return np.vstack((x, y)).T

    def create_tooth(self):
        pitch_radius = self.pitch_diameter / 2
        base_radius = self.base_diameter / 2
        outer_radius = pitch_radius + self.addendum
        root_radius = pitch_radius - self.dedendum

        involute = self.involute_profile(base_radius, outer_radius)
        mirrored = np.copy(involute)
        mirrored[:, 1] *= -1

        arc = []
        arc_steps = 10
        start_angle = np.arctan2(mirrored[-1, 1], mirrored[-1, 0])
        end_angle = -start_angle
        for i in range(arc_steps + 1):
            angle = start_angle + (end_angle - start_angle) * i / arc_steps
            x = root_radius * cos(angle)
            y = root_radius * sin(angle)
            arc.append([x, y])

        profile = np.vstack([involute, arc, mirrored[::-1]])
        if not np.allclose(profile[0], profile[-1]):
            profile = np.vstack([profile, profile[0]])
        logging.debug(f"Created tooth profile with {len(profile)} points")
        return profile

    def mesh(self):
        tooth_profile = self.create_tooth()
        polygon = Polygon(tooth_profile)
        if not polygon.is_valid:
            polygon = polygon.buffer(0)
            logging.warning("Tooth polygon was invalid, repaired with buffer")

        tooth_mesh = trimesh.creation.extrude_polygon(polygon, self.width, engine='triangle')
        logging.debug(f"Extruded tooth mesh with {len(tooth_mesh.vertices)} vertices")

        all_teeth = []
        for i in range(self.teeth):
            angle = 2 * pi * i / self.teeth
            rot = trimesh.transformations.rotation_matrix(angle, [0, 0, 1])
            rotated_tooth = tooth_mesh.copy().apply_transform(rot)
            all_teeth.append(rotated_tooth)
            logging.debug(f"Added tooth {i+1}/{self.teeth}")

        gear_body = trimesh.util.concatenate(all_teeth)
        logging.debug(f"Combined {self.teeth} teeth into gear body with {len(gear_body.vertices)} vertices")

        bore = trimesh.creation.cylinder(radius=self.bore_diameter / 2, height=self.width + 0.1)
        bore.apply_translation([0, 0, self.width / 2])
        gear = gear_body.difference(bore, engine='scad')
        logging.debug(f"Subtracted bore, resulting mesh has {len(gear.vertices)} vertices")

        if self.hole_count > 0:
            hole_cylinders = []
            for i in range(self.hole_count):
                angle = 2 * pi * i / self.hole_count
                x = cos(angle) * self.hole_radius
                y = sin(angle) * self.hole_radius
                hole = trimesh.creation.cylinder(radius=self.hole_diameter / 2, height=self.width + 0.1)
                hole.apply_translation([x, y, self.width / 2])
                if not hole.is_volume:
                    hole = hole.convex_hull
                hole_cylinders.append(hole)
            gear = gear.difference(hole_cylinders, engine='scad')
            logging.debug(f"Subtracted {self.hole_count} holes, resulting mesh has {len(gear.vertices)} vertices")

        if not gear.is_watertight:
            logging.warning("Final gear mesh is not watertight")
        else:
            logging.info("Final gear mesh is watertight")

        return gear