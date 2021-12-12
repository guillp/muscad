difference() {
  // attachment
  // volume
  translate(v=[0, 0, -15.2])
  cube(size=[34.4, 30.4, 8.0], center=true);
  // bearing
  union() {
    // base
    // volume
    cube(size=[34.4, 30.4, 22.4], center=true);
    // bolts
    union() {
      translate(v=[-12.0, -9.0, -10.62])
      union() {
        // thread
        cylinder(h=10, d=4.378, $fn=34, center=true);
        // head
        translate(v=[0, 0, -6.78])
        cylinder(h=3.6, d=8.5, $fn=66, center=true);
        // head_clearance
        translate(v=[0, 0, -58.56])
        cylinder(h=100, d=8.5, $fn=66, center=true);
      }
      translate(v=[-12.0, 9.0, -10.62])
      union() {
        // thread
        cylinder(h=10, d=4.378, $fn=34, center=true);
        // head
        translate(v=[0, 0, -6.78])
        cylinder(h=3.6, d=8.5, $fn=66, center=true);
        // head_clearance
        translate(v=[0, 0, -58.56])
        cylinder(h=100, d=8.5, $fn=66, center=true);
      }
      translate(v=[12.0, -9.0, -10.62])
      union() {
        // thread
        cylinder(h=10, d=4.378, $fn=34, center=true);
        // head
        translate(v=[0, 0, -6.78])
        cylinder(h=3.6, d=8.5, $fn=66, center=true);
        // head_clearance
        translate(v=[0, 0, -58.56])
        cylinder(h=100, d=8.5, $fn=66, center=true);
      }
      translate(v=[12.0, 9.0, -10.62])
      union() {
        // thread
        cylinder(h=10, d=4.378, $fn=34, center=true);
        // head
        translate(v=[0, 0, -6.78])
        cylinder(h=3.6, d=8.5, $fn=66, center=true);
        // head_clearance
        translate(v=[0, 0, -58.56])
        cylinder(h=100, d=8.5, $fn=66, center=true);
      }
    }
  }
}
