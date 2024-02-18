#include<stdio.h>
int main() {
	int niz[100-1+1] ;
	int i;
	int j;
	int n;
	int temp;
	scanf("%d",&n);
	for (i = 1;i<=n;i++){
		scanf("%d",&niz[i-1]);
		}
	for (i = 1;i<=n;i++){
		for (j = i+1;j<=n;j++){
			if (niz[i-1]<=niz[j-1]){
				continue;
				}else{
				temp = niz[i-1];
				niz[i-1] = niz[j-1];
				niz[j-1] = temp;
				}
			}
		}
	for (i = 1;i<=n;i++){
		printf("%d",niz[i-1]);
		printf(" ");
		}
	}
