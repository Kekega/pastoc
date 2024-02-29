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
	int _resa718;
	if (exponent == 0){
		_resa718 = 1;
		}else{
		_resa718 = base*recursivePower(base, exponent-1);
		}
	return _resa718;
	}