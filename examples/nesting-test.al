BEGIN
   int a;
   a := 2;
   printi(a);
   println();
   BEGIN
      int a;
      a := 3;
      printi(a);
      println();
   end;
   printi(a);
   println();
   BEGIN
      a := a + 4;
      printi(a);
      println();
      begin
      Begin
        int b;
      	b := a + 5;
	printi(a);
	println();
      	Begin
		printi(b);   # referring to the outer scope
		println();
       	 	int b;
                b := 0;	     # in the local scope
      		a := a + 17;
		printi(a);
		println();
		printi(b);
		println();
      	end;
	printi(b);
        println();
	end;
      end;
      #printi(b);   # this was caught correctly and flagged as an error
    END;
   printi(a);
end
