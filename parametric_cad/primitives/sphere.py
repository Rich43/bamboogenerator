import trimesh

class Sphere:
    def __init__(self, radius, subdivisions=3):
        self.radius = radius
        self.subdivisions = subdivisions
        self._position = (0, 0, 0)

    def at(self, x, y, z):
        self._position = (x, y, z)
        return self

    def mesh(self):
        sph = trimesh.creation.icosphere(subdivisions=self.subdivisions,
                                         radius=self.radius)
        sph.apply_translation(self._position)
        return sph
