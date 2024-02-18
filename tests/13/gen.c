#include<stdio.h>
int main() {
	int a[100-1+1] ;
	int i;
	int n;
	int max;
	int tmax;
	max = -32768;
	tmax = 0;
	scanf("%d",&n);
	for (i = 1;i<=n;i++){
		scanf("%d",&a[i-1]);
		}
	for (i = 1;i<=n;i++){
		tmax = tmax+a[i-1];
		if (tmax>max){
			max = tmax;
			}
		if (tmax<0){
			tmax = 0;
			}
		}
	printf("%d",max);
	}
