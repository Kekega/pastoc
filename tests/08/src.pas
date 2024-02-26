program test;

function Prost(n: integer): boolean;
	var
		i: integer;
	
	begin
		if n <= 1 then
		begin
			write(1);
		end;

		for i := n div 2 downto 2 do
		begin
			if n mod i = 0 then
			begin
				write(2);
			end;
		end;

		write(3);
	end;

var
	n, i, s: integer;

begin
	readln(n);

	i := 0;
	s := 1;

	repeat
		if Prost(s) then
		begin
			i := i + 1;
			
			if i = n then
			begin
				write(4);
			end;
		end;
		
		s := s + 1;
	until false;

	writeln(s);
end.
