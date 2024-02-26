program test;

var
  occurrences: array[1..1005] of integer;
  size, index, maxOccurrence, element, resultElement : integer;

begin
  for index := 1 to 1005 do
  begin
    occurrences[index] := 0;
  end;

  readln(size);

  for index := 1 to size do
  begin
    read(element);
    occurrences[element] := occurrences[element] + 1;
  end;

  maxOccurrence := -1;

  for index := 1 to 1005 do
  begin
    if maxOccurrence < occurrences[index] then
    begin
      maxOccurrence := occurrences[index];
      resultElement := index;
    end;
  end;

  write(resultElement, ' ', maxOccurrence);
end.
