program test;

var
	a, b: real;

begin
	readln(a, b);
    if (2*a > b + 1) and ((b > 1) or (b > 2)) then
        write(a, b);
end.
