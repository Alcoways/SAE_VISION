d1=22;
d2=10;
u=30;
v=50;
c1=[0,0,0];
c2=[1,1,1];
l_table=100;
l_mire=80;
mire=1;
taille_coin=3;

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

if (mire==1){
    color("white") translate([(l_table-l_mire)/2-taille_coin-2,(l_table-l_mire)/2-taille_coin-2,0]) cube([l_mire+2*taille_coin+4,l_mire+2*taille_coin+4,2]);
    color("black") {
        translate([(l_table-l_mire)/2,(l_table-l_mire)/2, 2]) {
            cube([taille_coin, taille_coin, 0.001]);
            translate([-taille_coin,-taille_coin,0]) cube([taille_coin, taille_coin, 0.001]);
        }

        translate([l_table-taille_coin-(l_table-l_mire)/2,l_table-taille_coin-(l_table-l_mire)/2, 2]) {
            cube([taille_coin, taille_coin, 0.001]);
            translate([taille_coin,taille_coin,0]) cube([taille_coin, taille_coin, 0.001]);
        }
        
        translate([l_table-taille_coin-(l_table-l_mire)/2,(l_table-l_mire)/2, 2]) {
            cube([taille_coin, taille_coin, 0.001]);
            translate([taille_coin,-taille_coin,0]) cube([taille_coin, taille_coin, 0.001]);
        }

        translate([(l_table-l_mire)/2,l_table-taille_coin-(l_table-l_mire)/2, 2]) {
            cube([taille_coin, taille_coin, 0.001]);
            translate([-taille_coin,taille_coin,0]) cube([taille_coin, taille_coin, 0.001]);
        }
    }
    
}


color([74/255,67/255,75/255],1) translate([0,0,-l_table]) cube(l_table);

