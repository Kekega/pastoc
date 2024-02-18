#include<stdio.h>
int pow_rek(int a, int b);
int main() {
	int a;
	int b;
	scanf("%d",&a);
	scanf("%d",&b);
	printf("%d",pow_rek(a, b));
	printf("\n");
	}
int pow_rek(int a, int b){
	int _res9e7c0f8e;
	if (b == 0){
		exit(1);
		}
	exit(a*pow_rek(a, b-1));
	return _res9e7c0f8e;
	}