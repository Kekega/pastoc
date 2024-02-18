#include<stdio.h>
char ExtractOnesDigit(char s);
char ExtractTensDigit(char s);
char ExtractHundredsDigit(char s);
int main() {
	char input[100] = {0};
	char output[100] = {0};
	char currentChar;
	char digit;
	int i;
	int outputIndex;
	int inputLength;
	scanf("%s",input);
	i = 1;
	outputIndex = 1;
	inputLength = strlen(input);
	while (i<=inputLength){
		currentChar = input[i-1];
		i++;
		digit = ExtractHundredsDigit(currentChar);
		if (digit != '0' || digit == '0' && outputIndex>1){
			output[outputIndex-1] = digit;
			outputIndex++;
			}
		output[outputIndex-1] = ExtractTensDigit(currentChar);
		outputIndex++;
		output[outputIndex-1] = ExtractOnesDigit(currentChar);
		outputIndex++;
		}
	printf("%s",output);
	}
char ExtractHundredsDigit(char s){
	char _res39be44bc;
	if (s<100){
		exit('0');
		}else{
		exit('0'+s / 100);
		}
	return _res39be44bc;
	}
char ExtractTensDigit(char s){
	char _res3446da45;
	if (s<10){
		exit('0');
		}else{
		exit('0'+s / 10 % 10);
		}
	return _res3446da45;
	}
char ExtractOnesDigit(char s){
	char _res726dc6f7;
	exit('0'+s % 10);
	return _res726dc6f7;
	}