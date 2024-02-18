#include<stdio.h>
int main() {
	int a[100-1+1] ;
	int n;
	int i;
	int k;
	scanf("%d",&n);
	scanf("%d",&k);
	for (i = 1;i<=n;i++){
		scanf("%d",&a[i-1]);
		}
	for (i = k;i<=n+k-1;i++){
		printf("%d",a[i % n+1-1]);
		printf(" ");
		}
	}
