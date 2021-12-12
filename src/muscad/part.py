from __future__ import annotations

import typing
from itertools import chain

from muscad import back
from muscad import bottom
from muscad import Composite
from muscad import EE
from muscad import front
from muscad import Hole
from muscad import left
from muscad import List
from muscad import Misc
from muscad import Object
from muscad import render_comment
from muscad import right
from muscad import top
from muscad import Union


def walk_mro_until(cls, supercls):
    for c in cls.mro():
        if c == supercls:
            break
        yield c


class Part(Composite):
    """
    Helper class to build complex objects.
    A Part is made of 3 kind of objects:
    - instances of Object, which will form the "main" structure of this Part
    - instances of Misc, which are miscellaneous items that will not be taken into account when evaluating this Part dimensions
    - instances of Hole, which will be "unfillable" holes which will be substracted from that Part.

    Those objects can be added to that Part using add_child(), add_misc() or add_hole().
    All class attributes that are instances of Object, Misc or Hole will be added to all instances of this Part.
    """

    def __init_subclass__(cls, **kwargs: typing.Any) -> None:
        """
        When creating an inherited class, sort all class-level attributes and make lists of all Objects, Misc and Holes
        """
        super().__init_subclass__(**kwargs)
        cls.class_parts: List[Object] = []
        cls.class_misc: List[Object] = []
        cls.class_holes: List[Object] = []
        for class_ in walk_mro_until(cls, Part):
            for name, obj in class_.__dict__.items():
                if isinstance(obj, (Misc, Hole, Object)) and not name.startswith("_"):
                    cls._init_element(name, obj)

    @classmethod
    def _init_element(cls, name: str, obj: typing.Union[Misc, Hole, Object]):
        """
        Given a class level attribute, add it to the class level lists of misc/holes/parts.
        :param name: the attribute name
        :param obj: the attribute value
        :return:
        """
        if isinstance(obj, Misc):
            obj = obj.object
            if obj.comment is None:
                obj.comment = name
            cls.class_misc.append(obj)
        elif isinstance(obj, Hole):
            obj = obj.object
            if obj.comment is None:
                obj.comment = name
            cls.class_holes.append(obj)
        elif isinstance(obj, Object):
            if obj.comment is None:
                obj.comment = name
            cls.class_parts.append(obj)

    def __init__(
        self,
        *args: typing.Union[float, bool, Misc, Hole, Object],
        **kwargs: typing.Union[float, bool, Misc, Hole, Object],
    ):
        """
        When instanciating a Part, add the class level misc/holes/parts to the instance.
        :param args:
        :param kwargs:
        """
        super().__init__()
        self.children = self.class_parts.copy() if hasattr(self, "class_parts") else []
        self.holes = self.class_holes.copy() if hasattr(self, "class_holes") else []
        self.miscellaneous = (
            self.class_misc.copy() if hasattr(self, "class_misc") else []
        )
        self.init(*args, **kwargs)

    def init(
        self,
        *args: typing.Union[float, bool, Misc, Hole, Object],
        **kwargs: typing.Union[float, bool, Misc, Hole, Object],
    ) -> None:
        """
        Override this to add parametric children to this Part
        :param args:
        :param kwargs:
        :return:
        """
        for o in args:
            if isinstance(o, Misc):
                self.add_misc(o)
            elif isinstance(o, Hole):
                self.add_hole(o)
            elif isinstance(o, Object):
                self.add_child(o)
        for comment, o in kwargs.items():
            if isinstance(o, Misc):
                self.add_misc(o, comment)
            elif isinstance(o, Hole):
                self.add_hole(o, comment)
            elif isinstance(o, Object):
                self.add_child(o, comment)

    def add_child(self, obj: Object, comment: str = None) -> Object:
        if comment:
            obj.comment = comment
        super().add_child(obj)
        return self

    def add_hole(self, obj: typing.Union[Object, Hole], comment: str = None) -> Object:
        if isinstance(obj, Hole):
            obj = obj.object
        if comment:
            obj.comment = comment
        self.holes.append(obj)
        return self

    def add_misc(
        self, obj: typing.Union[Object, Misc, Hole], comment: str = None
    ) -> Object:
        if isinstance(obj, Misc):
            obj = obj.object
        if comment:
            obj.comment = comment
        self.miscellaneous.append(obj)
        return self

    def revert(self):
        """
        Turns all holes to children, and all children to holes.
        Note that misc items are untouched, so it probably makes no sense to revert a part containing misc items.
        :return: the same part, with holes and children reverted
        """
        self.children, self.holes = self.holes, self.children

    def __setattr__(self, key, value):
        previous = getattr(self, key, None)
        super().__setattr__(key, value)
        if key.startswith("_"):
            return
        elif isinstance(value, Misc):
            if value.comment is None:
                value.comment = key
            # if previous:
            #     self.miscellaneous.remove(previous)
            self.add_misc(value)
        elif isinstance(value, Hole):
            if value.comment is None:
                value.comment = key
            #            if previous:
            #               self.holes.remove(previous)
            self.add_hole(value)
        elif isinstance(value, Object):
            if value.comment is None:
                value.comment = key
            if previous:
                self.children.remove(previous)
            self.add_child(value)

    @render_comment
    def render(self, postprocess=True):
        if not self.children and not self.miscellaneous:
            if self.holes:
                self.children, self.holes = self.holes, self.children
            else:
                raise RuntimeError("This part has no children")
        # renders children and misc
        renderable = sum(chain(self.children, self.miscellaneous))
        # if this part has holes, render a diff of all children with all holes
        if self.holes:
            renderable -= self.holes
        # applies postprocessing
        if postprocess:
            renderable = self.postprocess(renderable)
        # applies the modifier
        return renderable.set_modifier(self.modifier).render()

    def postprocess(self, renderable: Object):
        """
        Applies some postprocessing transformation to the part, at render time.
        Postprocessing will not be taken into account when calculating this part dimension or position.
        You use it for example to position the Part to make printing easier.
        Postprocessing can be disabled by passing `postprocess=False` to ` render()`.
        This method can be overridden in subclasses. By default, it does nothing.
        :param renderable: the part to postprocess for rendering
        :return: the postprocessed renderable
        """
        return renderable

    def walk(self):
        yield from super().walk()
        for misc in self.miscellaneous:
            yield from misc.walk()

    @property
    def left(self):
        return left(self.children)

    @property
    def right(self):
        return right(self.children)

    @property
    def back(self):
        return back(self.children)

    @property
    def front(self):
        return front(self.children)

    @property
    def bottom(self):
        return bottom(self.children)

    @property
    def top(self):
        return top(self.children)

    def debug(self, include_misc: bool = False) -> Part:
        """
        Turn all children to debug, not the misc (Unless include_misc is set to True).
        """
        if include_misc:
            return super().debug(self)

        self.children = [child.debug() for child in self.children]
        return self


class MirroredPart(Part):
    def __init_subclass__(
        cls,
        x: bool = False,
        y: bool = False,
        z: bool = False,
        center_x: float = 0,
        center_y: float = 0,
        center_z: float = 0,
        keep_x: bool = False,
        keep_y: bool = False,
        keep_z: bool = False,
        **kwargs: typing.Dict[str, typing.Any],
    ):
        super().__init_subclass__(**kwargs)
        cls.mirror_x = x
        cls.mirror_y = y
        cls.mirror_z = z
        cls._center_x = center_x
        cls._center_y = center_y
        cls._center_z = center_z
        cls.keep_x = keep_x
        cls.keep_y = keep_y
        cls.keep_z = keep_z

    @render_comment
    def render(self) -> str:
        if not self.children:
            raise RuntimeError("This part has no children")
        children: Object = Union(self.children)
        if self.holes:
            children = children - self.holes
        if self.mirror_x:
            children = children.x_mirror(center=self._center_x, keep=self.keep_x)
        if self.mirror_y:
            children = children.y_mirror(center=self._center_y, keep=self.keep_y)
        if self.mirror_z:
            children = children.z_mirror(center=self._center_z, keep=self.keep_z)
        return Union(children, self.miscellaneous).set_modifier(self.modifier).render()

    @property
    def left(self) -> float:
        if self.mirror_x:
            if self.keep_x:
                return -max(abs(left(self.children)), abs(right(self.children)))
            return -right(self.children)
        return left(self.children)

    @property
    def right(self) -> float:
        if self.mirror_x:
            if self.keep_x:
                return max(abs(left(self.children)), abs(right(self.children)))
            return -left(self.children)
        return right(self.children)

    @property
    def back(self) -> float:
        if self.mirror_y:
            if self.keep_y:
                return -max(abs(back(self.children)), abs(front(self.children)))
            return -front(self.children)
        return back(self.children)

    @property
    def front(self) -> float:
        if self.mirror_y:
            if self.keep_y:
                return max(abs(back(self.children)), abs(front(self.children)))
            return -back(self.children)
        return front(self.children)

    @property
    def bottom(self) -> float:
        if self.mirror_z:
            if self.keep_z:
                return -max(abs(bottom(self.children)), abs(top(self.children)))
            return -top(self.children)
        return bottom(self.children)

    @property
    def top(self) -> float:
        if self.mirror_z:
            if self.keep_z:
                return max(abs(bottom(self.children)), abs(top(self.children)))
            return -bottom(self.children)
        return top(self.children)


from muscad.primitives import Square


class RotationalExtrudedPart(Part):
    """
    A part that will be transformed with a RotationalExtrusion as postprocessing.
    You must build your part flat along the Y axis and have the shape defined on the positive X axis.
    """

    def init(
        self,
        *args: typing.Union[Misc, Hole, Object],
        **kwargs: typing.Union[Misc, Hole, Object],
    ) -> None:
        # mask will hide the shape on negative X axis.
        mask = Square(width=self.width + EE, depth=self.depth + EE).align(
            right=self.center_x, center_y=self.center_y
        )
        self.add_hole(mask)

    def postprocess(self, renderable: Object) -> Object:
        return renderable.rotational_extrude()
