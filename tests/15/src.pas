function ExtractHundredsDigit(s: char): char;
begin
  if ord(s) < 100 then
  begin
    exit('0');
  end
  else
  begin
    exit(chr(ord('0') + ord(s) div 100));
  end;
end;

function ExtractTensDigit(s: char): char;
begin
  if ord(s) < 10 then
  begin
    exit('0');
  end
  else
  begin
    exit(chr(ord('0') + (ord(s) div 10) mod 10));
  end;
end;

function ExtractOnesDigit(s: char): char;
begin
  exit(chr(ord('0') + ord(s) mod 10));
end;

var
  input, output: string;
  currentChar, digit: char;
  i, outputIndex, inputLength: integer;

begin
  readln(input);

  i := 1;
  outputIndex := 1;

  inputLength := length(input);

  while i <= inputLength do
  begin
    currentChar := input[i];
    inc(i);

    digit := ExtractHundredsDigit(currentChar);

    if (digit <> '0') or (digit = '0') and (outputIndex > 1) then
    begin
      insert(digit, output, outputIndex);
      inc(outputIndex);
    end;

    insert(ExtractTensDigit(currentChar), output, outputIndex);
    inc(outputIndex);

    insert(ExtractOnesDigit(currentChar), output, outputIndex);
    inc(outputIndex);
  end;

  write(output);
end.
