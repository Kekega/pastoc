#include<stdio.h>
int f2(int b);
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
	int _res3b62abee;
	int f2(int b){
		int _res32702869;
		_res32702869 = b+1;
		return _res32702869;
		};
	_res3b62abee = a+f2(a);
	return _res3b62abee;
	}