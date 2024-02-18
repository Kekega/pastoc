#include<stdio.h>
void fun2(int a, int b);
void fun1(int a);
int main() {
	int n;
	scanf("%d",&n);
	if (n == 1){
		printf("x");
		}
	}
void fun1(int a){
	fun2(a, 999);
	}
void fun2(int a, int b){
	fun1(a+1);
	}