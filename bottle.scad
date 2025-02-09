$fn = 100; // Smooth appearance

module bottle_body() {
    difference() {
        cylinder(h=180, r=35);
        translate([0, 0, -1]) cylinder(h=182, r=32);
    }
}

module bottle_neck() {
    translate([0, 0, 180])
    difference() {
        cylinder(h=20, r1=30, r2=28);
        translate([0, 0, -1]) cylinder(h=22, r=26);
    }
}

module bottle_cap() {
    translate([0, 0, 200])
    difference() {
        cylinder(h=15, r=30);
        translate([0, 0, -1]) cylinder(h=17, r=27);
        // Simulated screw ridges
        for (i = [0:4]) {
            rotate([0, 0, i * 72]) translate([23, -3, 2 + i * 3])
            cube([6, 6, 2], center=true);
        }
    }
}

module water_bottle() {
    color("blue", 0.2) bottle_body(); // Transparent body
    color("gray") bottle_neck();
    color("black") bottle_cap();
}

water_bottle();
