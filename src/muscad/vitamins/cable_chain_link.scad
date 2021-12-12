union() {
  difference() {
    // cylinder
    translate(v=[0, 0, 0.5])
    cylinder(h=0.6, d=15.8, $fn=124, center=true);
    // tunnel
    translate(v=[0, 0, 0.5])
    cylinder(h=2.6, d=6.2, $fn=48, center=true);
  }
  difference() {
    // cylinder
    translate(v=[0, 0, 0.9])
    cylinder(h=1.8, d=15.8, $fn=124, center=true);
    // female
    difference() {
      // cylinder
      translate(v=[0, 0, 0.5])
      cylinder(h=1.4, d=16.2, $fn=127, center=true);
      // tunnel
      translate(v=[0, 0, 0.5])
      cylinder(h=3.4, d=5.8, $fn=45, center=true);
    }
  }
}
