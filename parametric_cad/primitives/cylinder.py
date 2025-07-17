from parametric_cad.core import tm

class Cylinder:
    def __init__(self, radius, height, sections=32):
        self.radius = radius
        self.height = height
        self.sections = sections
        self._position = (0, 0, 0)

    def at(self, x, y, z):
        self._position = (x, y, z)
        return self

    def mesh(self):
        cyl = tm.creation.cylinder(radius=self.radius, height=self.height,
                                   sections=self.sections)
        cyl.apply_translation(self._position)
        return cyl
