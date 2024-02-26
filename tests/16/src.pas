program test;

function f1(a : integer) : integer;
    var i: integer;
    function f2(b: integer) : integer;
        var c: integer;
        function f3(d: integer) : integer;
            begin
                b := b + 1;
            end;
        begin
            f3(4);
            f2 := b + c;
        end;
    begin        
        for i := 1 to 5 do
        begin
            f1 := f2(i);
        end;

    end;

var
	n, s: integer;


begin
	readln(n);

    s := f1(n);

    writeln(s);
end.