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
	int _res1c07c36a;
	if (exponent == 0){
		_res1c07c36a = 1;
		}else{
		_res1c07c36a = base*recursivePower(base, exponent-1);
		}
	return _res1c07c36a;
	}