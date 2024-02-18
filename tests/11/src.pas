var
  numbersA, numbersB, numbersC: array[1..100] of integer;
  size, indexA, indexB, indexC, i: integer;

begin
  indexB := 1;
  indexC := 1;

  readln(size);

  for indexA := 1 to size do
  begin
    read(numbersA[indexA]);
  end;

  for indexA := 1 to size do
  begin
    if numbersA[indexA] mod 2 = 0 then
    begin
      numbersB[indexB] := numbersA[indexA];
      indexB := indexB + 1;
    end
    else
    begin
      numbersC[indexC] := numbersA[indexA];
      indexC := indexC + 1;
    end;
  end;

  for i := 1 to indexB - 1 do
  begin
    write(numbersB[i], ' ');
  end;

  writeln();

  for i := 1 to indexC - 1 do
  begin
    write(numbersC[i], ' ');
  end;
end.
