begin
	printc('a');
println();
	if 1 == 1 then
		prints("1 == 1");
	fi;
	println();
	printc('b');
println();
	if 1 != 1 then
		prints("1 != 1");
	fi;
	println();
	printc('c');
	println();
	if 1 != 1 then
		prints("1 != 1");
	else
		prints("1 == 1");
	fi;	
println();
	printc('d');
	println();
	int a;
	a := 1;
	if  A != 1 then
		prints("1 != 1");
	else
		prints("1 == 1");
	fi;	
println();


	printc('e');
	println();
	if true then
		printb(true);
	else
		printb(FALSE);
	fi;	
println();


	printc('f');
	println();
	if 1 < 2 then
		prints("1 < 2");
	fi;	
println();


	printc('g');
	println();
	if 1 < 2 && 3 > 4 then
		prints("1 < 2 && 3 > 4");
	fi;	
println();


	printc('h');
	println();
	if (1 < 2) && (3 > 4) || true then
		prints("(1 < 2) && (3 > 4) || true");
	fi;	
println();


	printc('i');
	println();
	if true && true then
		prints("true && true");
	fi;	
println();
end
