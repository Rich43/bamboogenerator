from math import cos, pi, sin

from parametric_cad.core import safe_difference, tm
from .base import Primitive


class ChainSprocket(Primitive):
    """Simple chain sprocket for roller chain."""

    def __init__(
        self,
        pitch: float = 12.7,
        roller_diameter: float = 7.75,
        teeth: int = 16,
        thickness: float = 5.0,
        bore_diameter: float = 10.0,
        clearance: float = 0.5,
    ) -> None:
        super().__init__()
        self.pitch = float(pitch)
        self.roller_diameter = float(roller_diameter)
        self.teeth = int(teeth)
        self.thickness = float(thickness)
        self.bore_diameter = float(bore_diameter)
        self.clearance = float(clearance)

    @property
    def pitch_radius(self) -> float:
        return self.pitch / (2 * sin(pi / self.teeth))

    @property
    def pitch_diameter(self) -> float:
        return self.pitch_radius * 2

    def _create_mesh(self) -> tm.Trimesh:
        # Base disc sized so pockets can be subtracted
        outer_radius = self.pitch_radius + self.roller_diameter / 2 + self.clearance
        disc = tm.creation.cylinder(
            radius=outer_radius,
            height=self.thickness,
            sections=self.teeth * 4,
        )
        disc.apply_translation([0, 0, self.thickness / 2])

        bore = tm.creation.cylinder(radius=self.bore_diameter / 2, height=self.thickness + 0.1)
        bore.apply_translation([0, 0, self.thickness / 2])
        sprocket = safe_difference(disc, bore)

        pocket_radius = self.roller_diameter / 2 + self.clearance
        pockets = []
        for i in range(self.teeth):
            angle = 2 * pi * i / self.teeth
            x = cos(angle) * self.pitch_radius
            y = sin(angle) * self.pitch_radius
            pocket = tm.creation.cylinder(
                radius=pocket_radius,
                height=self.thickness + 0.1,
                sections=16,
            )
            pocket.apply_translation([x, y, self.thickness / 2])
            pockets.append(pocket)

        sprocket = safe_difference(sprocket, pockets)
        if not sprocket.is_watertight:
            repaired = sprocket.fill_holes()
            if repaired is not False:
                sprocket = repaired
            else:
                sprocket = sprocket.convex_hull
        return sprocket
