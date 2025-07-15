import trimesh

class ButtHinge:
    def __init__(self, leaf_length, pin_diameter):
        self.leaf_length = leaf_length
        self.pin_diameter = pin_diameter
        self._position = (0, 0, 0)

    def at(self, x, y, z):
        self._position = (x, y, z)
        return self

    def mesh(self):
        pin = trimesh.creation.cylinder(radius=self.pin_diameter/2, height=self.leaf_length)
        pin.apply_translation(self._position)
        return pin
