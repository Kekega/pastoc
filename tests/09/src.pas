function recursivePower(base, exponent: integer): integer;
begin
  if exponent = 0 then
  begin
    recursivePower := 1;
  end
  else 
  begin
	recursivePower := base * recursivePower(base, exponent - 1);
  end;
end;

var
  baseValue, exponentValue: integer;

begin
  readln(baseValue, exponentValue);

  writeln(recursivePower(baseValue, exponentValue));
end.
