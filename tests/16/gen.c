#include<stdio.h>
int f3(int d, int *a, int *_reseb8e, int *i, int *b, int *_resbb5b, int *c);
int f2(int b, int *a, int *_reseb8e, int *i);
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
	int _reseb8e;
	int i;
	for (i = 1;i<=5;i++){
		_reseb8e = f2(i, &a, &_reseb8e, &i);
		}
	return _reseb8e;
	}
int f3(int d, int *a, int *_reseb8e, int *i, int *b, int *_resbb5b, int *c){
	int _rese58e;
	*b = *b+1;
	return _rese58e;
	}
int f2(int b, int *a, int *_reseb8e, int *i){
	int _resbb5b;
	int c;
	f3(4, a, _reseb8e, i, &b, &_resbb5b, &c);
	_resbb5b = b+c;
	return _resbb5b;
	}