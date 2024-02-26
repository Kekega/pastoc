#include<stdio.h>
int f2(int b, int *a, int *_res13e0);
int f1(int a);
int main() {
	int n;
	int s;
	scanf("%d",&n);
	s = f1(n);
	printf("%d",s);
	printf("\n");
	}
int f1(int a){
	int _res13e0;
	_res13e0 = a+f2(a, &a, &_res13e0);
	return _res13e0;
	}
int f2(int b, int *a, int *_res13e0){
	int _rese223;
	_rese223 = b+1;
	return _rese223;
	}