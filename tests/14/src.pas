var
  arr: array[1..100] of integer;
  size, index, offset: integer;
begin
  readln(size, offset);

  for index := 1 to size do
  begin
    read(arr[index]);
  end;

  for index := offset to size + offset - 1 do
  begin
    write(arr[index mod size + 1], ' ');
  end;
end.
