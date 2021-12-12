from muscad import EE
from muscad import Part
from muscad.utils.volume import Volume


class CastBracket(Part):
    def init(self, width, height):
        self.body = Volume(width=width, depth=width, height=height)
        self.clearance = (
            ~Volume(width=width * 1.25, depth=width * 1.25, height=height + EE)
            .z_rotate(45)
            .align(
                center_x=self.body.right,
                center_y=self.body.front,
                center_z=self.body.center_z,
            )
        )

    @classmethod
    def bracket3030(cls):
        return cls(width=36, height=28)
