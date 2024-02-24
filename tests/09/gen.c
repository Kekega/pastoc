#include<stdio.h>
int recursivePower(int base, int exponent);
int main() {
	int baseValue;
	int exponentValue;
	scanf("%d",&baseValue);
	scanf("%d",&exponentValue);
	printf("%d",recursivePower(baseValue, exponentValue));
	printf("\n");
	}
int recursivePower(int base, int exponent){
	int _resbafd69fc;
	if (exponent == 0){
		_resbafd69fc = 1;
		}else{
		_resbafd69fc = base*recursivePower(base, exponent-1);
		}
	return _resbafd69fc;
	}