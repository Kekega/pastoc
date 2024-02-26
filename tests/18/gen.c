#include<stdio.h>
int f2(int b, int *a, int *_resd714, int *i);
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
	int _resd714;
	int i;
	for (i = 1;i<=5;i++){
		_resd714 = f2(i, &a, &_resd714, &i);
		}
	return _resd714;
	}
int f2(int b, int *a, int *_resd714, int *i){
	int _res12f4;
	_res12f4 = b+1;
	return _res12f4;
	}