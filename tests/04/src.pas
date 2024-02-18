procedure check_arm(x, cj, cd, cs: integer);
	var
		arm: boolean;

	begin
		if x < 0 then
		begin
			exit;
		end;

		arm := x = cj * cj * cj + cd * cd * cd + cs * cs * cs;

		if arm then
		begin
			write('YES');
		end
		else
		begin
			write('NO');
		end;
	end;

var
	j, cj, cd, cs: integer;

begin
	readln(j);

	cj := j mod 10;
	cd := (j div 10) mod 10;
	cs := (j div 100) mod 10;

	check_arm(j, cj, cd, cs);
end.
