function f1(a: integer) : integer;
    var i: integer;
    function f2(b: integer) : integer;
    begin
        f2 := b + 1;
    end;
    begin        
        for i := 1 to 5 do
        begin
            f1 := a + 1;
        end;

    end;

var
	n, s: integer;


begin
	readln(n);

    s := f1(n);

    writeln(s);
end.