BEGIN
   INT a;
   char b;
BooLean ccc;
String d;
   a := 1;
   b := 'a';
   ccc := False;
   d := "Hello, World!";
   printi(a);
   println();
   printc(b);
   println();
   prints(d);
   println();
   printb(ccc);
   println();
   printb(1 == 1);
   println();
   printb(1 == 2);
   println();
   printb(1 != 1);
   println();
   printb(1 != 2);
   println();
   printb(1 < 2);
   println();
   printb(1 > 2);
   println();
   printb(1 == 1 && 2 < 3);
   println();
   printi(10 * 2);
   println();
   a := 6 / 3;
   printi(a);
   println();
   a := a + 42;
   printi(a);
   println();
   a := a - 23;
   printb(a == 21);
   println();
   printi(a + (2 * 3 * a) + a / 2);

end
