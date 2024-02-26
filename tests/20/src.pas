program test;

function AddTwoNumbers(a, b: integer): integer;
begin
  AddTwoNumbers := a + b;
end;

var
  result: integer;

begin
  result := AddTwoNumbers(5, 7);
  writeln('The sum is: ', result);
end.