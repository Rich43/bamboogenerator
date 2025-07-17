from parametric_cad.core import tm

class Box:
    def __init__(self, width, depth, height):
        self.width = width
        self.depth = depth
        self.height = height
        self._position = (0, 0, 0)

    def at(self, x, y, z):
        self._position = (x, y, z)
        return self

    def mesh(self):
        box = tm.creation.box(extents=(self.width, self.depth, self.height))
        box.apply_translation(self._position)
        return box
