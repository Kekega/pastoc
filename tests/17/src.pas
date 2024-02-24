function f1(a: integer) : integer;
    function f2(b: integer) : integer;
    begin
        f2 := b + 1;
    end;
    begin        
        f1 := a + f2(a);
    end;

var
	n, s: integer;


begin
	readln(n);

    s := f1(n);

    writeln(s);
end.