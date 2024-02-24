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
	int _res7b8c1391;
	int i;
	int f2(int b){
		int _resf73f757e;
		_resf73f757e = b+1;
		return _resf73f757e;
		};
	for (i = 1;i<=5;i++){
		_res7b8c1391 = f2(i);
		}
	return _res7b8c1391;
	}