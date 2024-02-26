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
	int _res5346;
	if (exponent == 0){
		_res5346 = 1;
		}else{
		_res5346 = base*recursivePower(base, exponent-1);
		}
	return _res5346;
	}