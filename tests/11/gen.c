#include<stdio.h>
int main() {
	int numbersA[100-1+1] ;
	int numbersB[100-1+1] ;
	int numbersC[100-1+1] ;
	int size;
	int indexA;
	int indexB;
	int indexC;
	int i;
	indexB = 1;
	indexC = 1;
	scanf("%d",&size);
	for (indexA = 1;indexA<=size;indexA++){
		scanf("%d",&numbersA[indexA-1]);
		}
	for (indexA = 1;indexA<=size;indexA++){
		if (numbersA[indexA-1] % 2 == 0){
			numbersB[indexB-1] = numbersA[indexA-1];
			indexB = indexB+1;
			}else{
			numbersC[indexC-1] = numbersA[indexA-1];
			indexC = indexC+1;
			}
		}
	for (i = 1;i<=indexB-1;i++){
		printf("%d",numbersB[i-1]);
		printf(" ");
		}
	printf("\n");
	for (i = 1;i<=indexC-1;i++){
		printf("%d",numbersC[i-1]);
		printf(" ");
		}
	}
