"""Tests for the Volume class."""

from muscad import E, Object, Text, Volume


def test_volume() -> None:
    """Basic bounding box tests."""
    left = -12
    right = 10
    back = -22
    front = 20
    bottom = -33
    top = 30

    ref = Volume(left=left, right=right, back=back, front=front, bottom=bottom, top=top)

    assert ref.left == left
    assert ref.right == right
    assert ref.back == back
    assert ref.front == front
    assert ref.bottom == bottom
    assert ref.top == top

    front_to_top = ref.front_to_top()
    assert front_to_top.left == -right
    assert front_to_top.right == -left
    assert front_to_top.back == bottom
    assert front_to_top.front == top
    assert front_to_top.bottom == back
    assert front_to_top.top == front

    bottom_to_left = ref.bottom_to_left()
    assert bottom_to_left.left == bottom
    assert bottom_to_left.right == top
    assert bottom_to_left.back == -right
    assert bottom_to_left.front == -left
    assert bottom_to_left.bottom == -front
    assert bottom_to_left.top == -back

    front_to_right = ref.front_to_right()
    assert front_to_right.left == back
    assert front_to_right.right == front
    assert front_to_right.back == -right
    assert front_to_right.front == -left
    assert front_to_right.bottom == bottom
    assert front_to_right.top == top

    upside_down = ref.upside_down()
    assert upside_down.left == -right
    assert upside_down.right == -left
    assert upside_down.back == back
    assert upside_down.front == front
    assert upside_down.bottom == -top
    assert upside_down.top == -bottom

    upside_down_x = ref.upside_down(x_axis=True)
    assert upside_down_x.left == left
    assert upside_down_x.right == right
    assert upside_down_x.back == -front
    assert upside_down_x.front == -back
    assert upside_down_x.bottom == -top
    assert upside_down_x.top == -bottom

    front_to_back = ref.front_to_back()
    assert front_to_back.left == -right
    assert front_to_back.right == -left
    assert front_to_back.back == -front
    assert front_to_back.front == -back
    assert front_to_back.bottom == bottom
    assert front_to_back.top == top

    front_to_bottom = ref.front_to_bottom()
    assert front_to_bottom.left == -right
    assert front_to_bottom.right == -left
    assert front_to_bottom.back == -top
    assert front_to_bottom.front == -bottom
    assert front_to_bottom.bottom == -front
    assert front_to_bottom.top == -back

    bottom_to_right = ref.bottom_to_right()
    assert bottom_to_right.left == -top
    assert bottom_to_right.right == -bottom
    assert bottom_to_right.back == left
    assert bottom_to_right.front == right
    assert bottom_to_right.bottom == -front
    assert bottom_to_right.top == -back

    front_to_right = ref.front_to_right()
    assert front_to_right.left == back
    assert front_to_right.right == front
    assert front_to_right.back == -right
    assert front_to_right.front == -left
    assert front_to_right.bottom == bottom
    assert front_to_right.top == top

    back_to_right = ref.back_to_right()
    assert back_to_right.left == -front
    assert back_to_right.right == -back
    assert back_to_right.back == left
    assert back_to_right.front == right
    assert back_to_right.bottom == bottom
    assert back_to_right.top == top

    back_to_bottom = ref.back_to_bottom()
    assert back_to_bottom.left == left
    assert back_to_bottom.right == right
    assert back_to_bottom.back == -top
    assert back_to_bottom.front == -bottom
    assert back_to_bottom.bottom == back
    assert back_to_bottom.top == front

    left_to_bottom = ref.left_to_bottom()
    assert left_to_bottom.left == -front
    assert left_to_bottom.right == -back
    assert left_to_bottom.back == -top
    assert left_to_bottom.front == -bottom
    assert left_to_bottom.bottom == left
    assert left_to_bottom.top == right

    left_to_top = ref.left_to_top()
    assert left_to_top.left == -front
    assert left_to_top.right == -back
    assert left_to_top.back == bottom
    assert left_to_top.front == top
    assert left_to_top.bottom == -right
    assert left_to_top.top == -left

    left_to_front = ref.left_to_front()
    assert left_to_front.left == back
    assert left_to_front.right == front
    assert left_to_front.back == -right
    assert left_to_front.front == -left
    assert left_to_front.bottom == bottom
    assert left_to_front.top == top

    left_to_back = ref.left_to_back()
    assert left_to_back.left == -front
    assert left_to_back.right == -back
    assert left_to_back.back == left
    assert left_to_back.front == right
    assert left_to_back.bottom == bottom
    assert left_to_back.top == top

    right_to_bottom = ref.right_to_bottom()
    assert right_to_bottom.left == back
    assert right_to_bottom.right == front
    assert right_to_bottom.back == -top
    assert right_to_bottom.front == -bottom
    assert right_to_bottom.bottom == -right
    assert right_to_bottom.top == -left

    right_to_top = ref.right_to_top()
    assert right_to_top.left == -front
    assert right_to_top.right == -back
    assert right_to_top.back == -top
    assert right_to_top.front == -bottom
    assert right_to_top.bottom == left
    assert right_to_top.top == right

    right_to_front = ref.right_to_front()
    assert right_to_front.left == -front
    assert right_to_front.right == -back
    assert right_to_front.back == left
    assert right_to_front.front == right
    assert right_to_front.bottom == bottom
    assert right_to_front.top == top

    right_to_back = ref.right_to_back()
    assert right_to_back.left == back
    assert right_to_back.right == front
    assert right_to_back.back == -right
    assert right_to_back.front == -left
    assert right_to_back.bottom == bottom
    assert right_to_back.top == top

    x = 26
    y = 34
    z = 45
    translated = ref.translate(x=x, y=y, z=z)
    assert translated.left == left + x
    assert translated.right == right + x
    assert translated.back == back + y
    assert translated.front == front + y
    assert translated.bottom == bottom + z
    assert translated.top == top + z


def test_reverse_fillet() -> None:
    """Test for a chamfered Cube."""
    cube: Object = (
        Volume(width=50, depth=50, height=50)
        .reverse_fillet_left()
        .reverse_fillet_right()
        .reverse_fillet_back()
        .reverse_fillet_front()
        .reverse_fillet_bottom()
        .reverse_fillet_top()
    )
    cube -= Text("top", halign="center", valign="center").z_linear_extrude(1, top=cube.top + E)
    cube -= Text("bottom", halign="center", valign="center").z_linear_extrude(1, bottom=cube.bottom - E, downwards=True)
    cube -= Text("right", halign="center", valign="center").x_linear_extrude(1, right=cube.right + E)
    cube -= Text("left", halign="center", valign="center").x_linear_extrude(1, left=cube.left - E, leftwards=True)
    cube -= Text("front", halign="center", valign="center").y_linear_extrude(1, front=cube.front + E)
    cube -= Text("back", halign="center", valign="center").y_linear_extrude(1, back=cube.back - E, backwards=True)

    assert (
        cube.render()
        == """\
difference() {
  union() {
    // volume
    cube(size=[50.0, 50.0, 50.0], center=true);
    // left_top_edge
    translate(v=[-23.0, 0, 26.98])
    rotate(a=[180, 0, 0])
    translate(v=[0, -25.0, 0])
    rotate(a=[270, 180, 0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // left_bottom_chamfer
    translate(v=[-23.0, -25.0, -26.98])
    rotate(a=[270, 180, 0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // left_back_chamfer
    translate(v=[-23.0, -26.98, 0])
    rotate(a=[0, 0, 90])
    translate(v=[0, 0, -25.0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // left_front_chamfer
    translate(v=[-23.0, 26.98, 0])
    rotate(a=[0, 0, 180])
    translate(v=[0, 0, -25.0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // back_right_edge
    translate(v=[26.98, -23.0, 0])
    rotate(a=[0, 0, 180])
    translate(v=[0, 0, -25.0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // back_left_edge
    translate(v=[-26.98, -23.0, 0])
    rotate(a=[0, 0, 270])
    translate(v=[0, 0, -25.0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // right_top_edge
    translate(v=[23.0, 0, 26.98])
    rotate(a=[180, 0, 180])
    translate(v=[0, -25.0, 0])
    rotate(a=[270, 180, 0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // right_bottom_edge
    translate(v=[23.0, 0, -26.98])
    rotate(a=[0, 0, 180])
    translate(v=[0, -25.0, 0])
    rotate(a=[270, 180, 0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // right_back_edge
    translate(v=[23.0, -26.98, -25.0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // right_front_edge
    translate(v=[23.0, 26.98, 0])
    rotate(a=[0, 0, 270])
    translate(v=[0, 0, -25.0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // back_top_edge
    translate(v=[0, -23.0, 26.98])
    rotate(a=[180, 0, 0])
    translate(v=[-25.0, 0, 0])
    rotate(a=[90, 0, 90])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // back_bottom_edge
    translate(v=[0, -23.0, -26.98])
    rotate(a=[90, 0, 0])
    translate(v=[-25.0, 0, 0])
    rotate(a=[90, 0, 90])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // front_top_edge
    translate(v=[0, 23.0, 26.98])
    rotate(a=[270, 0, 0])
    translate(v=[-25.0, 0, 0])
    rotate(a=[90, 0, 90])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // front_bottom_edge
    translate(v=[-25.0, 23.0, -26.98])
    rotate(a=[90, 0, 90])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // front_right_edge
    translate(v=[26.98, 23.0, 0])
    rotate(a=[0, 0, 90])
    translate(v=[0, 0, -25.0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // front_left_edge
    translate(v=[-26.98, 23.0, -25.0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // bottom_front_edge
    translate(v=[0, 26.98, -23.0])
    rotate(a=[180, 0, 0])
    translate(v=[-25.0, 0, 0])
    rotate(a=[90, 0, 90])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // bottom_back_egde
    translate(v=[0, -26.98, -23.0])
    rotate(a=[270, 0, 0])
    translate(v=[-25.0, 0, 0])
    rotate(a=[90, 0, 90])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // bottom_right_edge
    translate(v=[26.98, 0, -23.0])
    rotate(a=[180, 0, 0])
    translate(v=[0, -25.0, 0])
    rotate(a=[270, 180, 0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // bottom_left_edge
    translate(v=[-27.02, 0, -23.0])
    rotate(a=[180, 0, 180])
    translate(v=[0, -25.0, 0])
    rotate(a=[270, 180, 0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // top_front_edge
    translate(v=[0, 26.98, 23.0])
    rotate(a=[90, 0, 0])
    translate(v=[-25.0, 0, 0])
    rotate(a=[90, 0, 90])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // top_back_edge
    translate(v=[-25.0, -26.98, 23.0])
    rotate(a=[90, 0, 90])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // top_right_edge
    translate(v=[26.98, -25.0, 23.0])
    rotate(a=[270, 180, 0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // top_left_edge
    translate(v=[-26.98, 0, 23.0])
    rotate(a=[0, 0, 180])
    translate(v=[0, -25.0, 0])
    rotate(a=[270, 180, 0])
    linear_extrude(height=50.0, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2, 2], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
  }
  translate(v=[0, 0, 24.02])
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  text(text="top", size=10, halign="center", valign="center");
  translate(v=[0, 0, -24.02])
  rotate(a=[180, 0, 0])
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  text(text="bottom", size=10, halign="center", valign="center");
  translate(v=[24.02, 0, 0])
  rotate(a=[90, 0, 90])
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  text(text="right", size=10, halign="center", valign="center");
  translate(v=[-24.02, 0, 0])
  rotate(a=[90, 0, 270])
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  text(text="left", size=10, halign="center", valign="center");
  translate(v=[0, 24.02, 0])
  rotate(a=[270, 180, 0])
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  text(text="front", size=10, halign="center", valign="center");
  translate(v=[0, -24.02, 0])
  rotate(a=[90, 0, 0])
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  text(text="back", size=10, halign="center", valign="center");
}"""
    )
