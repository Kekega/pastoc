#include<stdio.h>
int main() {
	int i;
	int j;
	int n;
	scanf("%d",&n);
	for (i = n;i>=1;i--){
		for (j = n-i;j>=1;j--){
			printf(" ");
			}
		for (j = 2*i-1;j>=1;j--){
			printf("*");
			}
		printf("\n");
		}
	}
