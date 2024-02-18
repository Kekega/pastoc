#include<stdio.h>
int main() {
	int arr[100-1+1] ;
	int size;
	int index;
	int offset;
	scanf("%d",&size);
	scanf("%d",&offset);
	for (index = 1;index<=size;index++){
		scanf("%d",&arr[index-1]);
		}
	for (index = offset;index<=size+offset-1;index++){
		printf("%d",arr[index % size+1-1]);
		printf(" ");
		}
	}
