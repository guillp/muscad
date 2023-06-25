from typing_extensions import Self

from muscad import TT, Cylinder, E, Object, Part, Union
from muscad.utils.volume import Volume


class Board(Part):
    def init(  # type: ignore[override]
        self, width: float, depth: float, height: float = 2, misc_height: float = 20
    ) -> None:
        self.board = Volume(
            center_x=0,
            width=width,
            center_y=0,
            depth=depth,
            center_z=0,
            height=height,
        )
        self.components = Volume(
            center_x=0,
            width=width,
            center_y=0,
            depth=depth,
            bottom=self.board.top,
            height=misc_height,
        )
        self.bolts = Union().misc()

    def add_bolt(self, bolt: Object, x: float, y: float) -> Self:
        if x < 0:
            x = self.board.right + x
        else:
            x = self.board.left + x

        if y < 0:
            y = self.board.front + y
        else:
            y = self.board.back + y
        self.bolts.add_child(bolt.align(center_x=x, center_y=y))
        return self

    @classmethod
    def mks_sbase(cls, bolt: Object | None = None) -> Self:
        board = cls(146.5, 95)
        if bolt:
            board.add_bolt(bolt, 4, 4)
            board.add_bolt(bolt, 4, -4)
            board.add_bolt(bolt, -4, -4)
            board.add_bolt(bolt, -4, 4)
        return board

    @classmethod
    def smps300rs(cls, bolt: Object | None = None) -> Self:
        board = cls(100, 100)
        if bolt:
            board.add_bolt(bolt, 4, 4)
            board.add_bolt(bolt, 4, -4)
            board.add_bolt(bolt, -4, -4)
            board.add_bolt(bolt, -4, 4)
        return board

    @classmethod
    def lcd12864(cls, bolt: Object | None = None) -> Self:
        lcd = cls(93, 70, height=1.5, misc_height=0)
        if bolt:
            lcd.add_bolt(bolt, 2.6, 2.6)
            lcd.add_bolt(bolt, -2.6, 2.6)
            lcd.add_bolt(bolt, 2.6, -2.6)
            lcd.add_bolt(bolt, -2.6, -2.6)
        lcd.screen = (
            Volume(width=78 + TT, depth=51 + TT, height=7)
            .fillet_height(r=0.4)
            .align(
                center_x=lcd.center_x,
                center_y=lcd.center_y,
                bottom=lcd.top - E,
            )
        )
        lcd.insert = Volume(
            width=5.5,
            depth=43,
            height=4,
            right=lcd.screen.left + E,
            center_y=lcd.screen.center_y,
            bottom=lcd.board.top - E,
        )
        lcd.connectors = Volume(
            width=49,
            depth=2,
            height=6,
            left=lcd.left + 14.1,
            center_y=lcd.back + 2.6,
            bottom=lcd.board.top - E,
        )
        lcd.lower_board = Volume(width=93, depth=87, height=1.5).align(
            center_x=lcd.center_x, front=lcd.front, top=lcd.bottom - 3
        )
        lcd.knob = Cylinder(d=7, h=25).align(
            center_x=lcd.lower_board.right - 10,
            center_y=lcd.lower_board.back + 8.53,
            bottom=lcd.lower_board.top - E,
        )
        lcd.buzzer = Cylinder(d=12, h=10).align(
            center_x=lcd.lower_board.right - 27.76,
            center_y=lcd.lower_board.back + 8.53,
            bottom=lcd.lower_board.top - E,
        )
        lcd.stop = Volume(
            width=6.1,
            depth=6.1,
            height=3,
            center_x=lcd.lower_board.left + 47.16,
            center_y=lcd.lower_board.back + 8.21,
            bottom=lcd.lower_board.top - E,
        )
        lcd.backlight = Cylinder(d=11.5, h=8).align(
            center_x=lcd.lower_board.left + 8,
            center_y=lcd.lower_board.back + 11.5,
            bottom=lcd.lower_board.top - E,
        )
        lcd.sd_card = Volume(
            width=40,
            depth=27,
            height=4.1,
            right=lcd.lower_board.left + 26,
            front=lcd.lower_board.front - 22.5,
            top=lcd.lower_board.bottom + E,
        ).misc()
        lcd.connectors = (
            Volume(
                width=22,
                depth=10,
                height=20,
                left=lcd.lower_board.left + 20,
                front=lcd.lower_board.front - 6,
                top=lcd.lower_board.bottom + E,
            )
            .fillet_height(r=1)
            .x_mirror(lcd.lower_board.center_x, keep=True)
            .misc()
        )
        return lcd

    @classmethod
    def raspberry_pi_3b(cls, bolt: Object | None = None) -> Self:
        board = cls(85, 56)
        if bolt:
            board.add_bolt(bolt, 3.5, 3.5)
            board.add_bolt(bolt, 3.5, -3.5)
            board.add_bolt(bolt, 61.5, -3.5)
            board.add_bolt(bolt, 61.5, 3.5)
        return board
