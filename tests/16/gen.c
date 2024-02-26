#include<stdio.h>
int f3(int d, int *a, int *_res47b3, int *i, int *b, int *_res3b1b, int *c);
int f2(int b, int *a, int *_res47b3, int *i);
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
	int _res47b3;
	int i;
	for (i = 1;i<=5;i++){
		_res47b3 = f2(i, &a, &_res47b3, &i);
		}
	return _res47b3;
	}
int f3(int d, int *a, int *_res47b3, int *i, int *b, int *_res3b1b, int *c){
	int _res813a;
	*b = *b+1;
	return _res813a;
	}
int f2(int b, int *a, int *_res47b3, int *i){
	int _res3b1b;
	int c;
	f3(4, a, _res47b3, i, &b, &_res3b1b, &c);
	_res3b1b = b+c;
	return _res3b1b;
	}