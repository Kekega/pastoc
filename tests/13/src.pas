program test;

var
  numbers: array[1..100] of integer;
  index, size, currentSum, maxSum : integer;

begin
  maxSum := -32768;
  currentSum := 0;

  readln(size);

  for index := 1 to size do
  begin
    read(numbers[index]);
  end;

  for index := 1 to size do
  begin
    currentSum := currentSum + numbers[index];

    if currentSum > maxSum then
    begin
      maxSum := currentSum;
    end;

    if currentSum < 0 then
    begin
      currentSum := 0;
    end;
  end;

  write(maxSum);
end.
