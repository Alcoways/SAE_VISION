d1=22;
d2=10;
u=10;
v=0;
c1=[1,0,0];
c2=[1,0,1];
l_table=100;
l_mire=50;
l_coin=10;
mire=0;

if (mire==0){
    translate([u,v,0]){
        color(c1,1){
            difference(){
                cylinder(2,r=d1/2,$fn=360);
                translate([0,0,-1]) cylinder(4,r=d2/2,$fn=360);
            }
        };
        color(c2,1) cylinder(2,r=d2/2,$fn=360);
    }
}

color("blue") translate([-l_table/2,-l_table/2,-l_table]) cube(l_table);

if (mire==1){
    difference(){
        difference(){
            difference(){
                difference(){
                    color("white") translate([-l_mire/2-5,-l_mire/2-5,-l_mire-8]) cube(l_mire+10);
                    translate([-l_mire/2-l_coin/2,-l_mire/2-l_coin/2,-l_coin+3]) cube(l_coin);
                };
                translate([-l_mire/2-l_coin/2,l_mire/2-l_coin/2,-l_coin+3]) cube(l_coin);   
            };
            translate([l_mire/2-l_coin/2,-l_mire/2-l_coin/2,-l_coin+3]) cube(l_coin);
        };
        translate([l_mire/2-l_coin/2,l_mire/2-l_coin/2,-l_coin+3]) cube(l_coin);    
    }

    color("black") translate([-l_mire/2-l_coin/2,-l_mire/2-l_coin/2,-l_coin+2]) cube(l_coin);
    color("black") translate([-l_mire/2-l_coin/2,l_mire/2-l_coin/2,-l_coin+2]) cube(l_coin);
    color("black") translate([l_mire/2-l_coin/2,-l_mire/2-l_coin/2,-l_coin+2]) cube(l_coin);
    color("black") translate([l_mire/2-l_coin/2,l_mire/2-l_coin/2,-l_coin+2]) cube(l_coin);
}