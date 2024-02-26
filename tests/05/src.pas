program test;

var
	c: char;
    l, h: boolean;
    d: integer;

begin
	readln(c);

    l := ord(c) >= ord('A');
    h := ord(c) <= ord('Z');

	if l and h then
	begin
		d := ord(c) + 32;
	end
	else
	begin
		d := ord(c) - 32;
	end;

    write(chr(d));
end.
