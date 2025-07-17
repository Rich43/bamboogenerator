import logging
from math import cos, pi, sin, tan
from typing import List

import numpy as np

from parametric_cad.core import safe_difference, tm
from parametric_cad.geometry import Polygon
from .base import Primitive

class SpurGear(Primitive):
    def __init__(
        self,
        module: float,
        teeth: int,
        width: float = 5.0,
        bore_diameter: float = 5.0,
        hole_count: int = 0,
        hole_diameter: float = 2.0,
        hole_radius: float | None = None,
    ) -> None:
        super().__init__()
        self.module = module
        self.teeth = teeth
        self.width = width
        self.bore_diameter = bore_diameter
        self.hole_count = hole_count
        self.hole_diameter = hole_diameter
        self.hole_radius = hole_radius or (self.pitch_diameter / 2 + module * 1.5)
        logging.debug(
            "Initialized SpurGear: module=%s, teeth=%s, width=%s, bore=%s, holes=%s",
            module,
            teeth,
            width,
            bore_diameter,
            hole_count,
        )

    @property
    def pitch_diameter(self) -> float:
        return self.module * self.teeth

    @property
    def base_diameter(self) -> float:
        pressure_angle = 20 * pi / 180
        return self.pitch_diameter * cos(pressure_angle)

    @property
    def addendum(self) -> float:
        return self.module

    @property
    def dedendum(self) -> float:
        return 1.25 * self.module

    def involute_profile(self, base_radius: float, outer_radius: float, steps: int = 10) -> np.ndarray:
        theta = np.linspace(0, np.arccos(base_radius / outer_radius), steps)
        x = base_radius * (np.cos(theta) + theta * np.tan(theta))
        y = base_radius * (np.sin(theta) - theta * np.tan(theta))
        return np.vstack((x, y)).T

    def create_tooth(self) -> np.ndarray:
        pitch_radius = self.pitch_diameter / 2
        base_radius = self.base_diameter / 2
        outer_radius = pitch_radius + self.addendum
        root_radius = pitch_radius - self.dedendum

        involute = self.involute_profile(base_radius, outer_radius)
        mirrored = np.copy(involute)
        mirrored[:, 1] *= -1

        arc: List[List[float]] = []
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
        logging.debug("Created tooth profile with %d points", len(profile))
        return profile

    def _create_mesh(self) -> tm.Trimesh:
        tooth_profile = self.create_tooth()
        polygon = Polygon(tooth_profile)
        if not polygon.is_valid:
            polygon = polygon.buffer(0)
            logging.warning("Tooth polygon was invalid, repaired with buffer")

        tooth_mesh = tm.creation.extrude_polygon(polygon, self.width, engine="triangle")
        logging.debug("Extruded tooth mesh with %d vertices", len(tooth_mesh.vertices))

        all_teeth = []
        for i in range(self.teeth):
            angle = 2 * pi * i / self.teeth
            rot = tm.transformations.rotation_matrix(angle, [0, 0, 1])
            rotated_tooth = tooth_mesh.copy().apply_transform(rot)
            all_teeth.append(rotated_tooth)
            logging.debug("Added tooth %d/%d", i + 1, self.teeth)

        gear_body = tm.util.concatenate(all_teeth)
        logging.debug(
            "Combined %d teeth into gear body with %d vertices",
            self.teeth,
            len(gear_body.vertices),
        )

        bore = tm.creation.cylinder(radius=self.bore_diameter / 2, height=self.width + 0.1)
        bore.apply_translation([0, 0, self.width / 2])
        gear = safe_difference(gear_body, bore)
        logging.debug("Subtracted bore, resulting mesh has %d vertices", len(gear.vertices))

        if self.hole_count > 0:
            hole_cylinders = []
            for i in range(self.hole_count):
                angle = 2 * pi * i / self.hole_count
                x = cos(angle) * self.hole_radius
                y = sin(angle) * self.hole_radius
                hole = tm.creation.cylinder(radius=self.hole_diameter / 2, height=self.width + 0.1)
                hole.apply_translation([x, y, self.width / 2])
                if not hole.is_volume:
                    hole = hole.convex_hull
                hole_cylinders.append(hole)
            gear = safe_difference(gear, hole_cylinders)
            logging.debug(
                "Subtracted %d holes, resulting mesh has %d vertices",
                self.hole_count,
                len(gear.vertices),
            )

        if not gear.is_watertight:
            logging.warning("Final gear mesh is not watertight")
        else:
            logging.info("Final gear mesh is watertight")

        return gear
