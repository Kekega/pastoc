#include<stdio.h>
int main() {
	int numbers[100-1+1] ;
	int index;
	int size;
	int currentSum;
	int maxSum;
	maxSum = -32768;
	currentSum = 0;
	scanf("%d",&size);
	for (index = 1;index<=size;index++){
		scanf("%d",&numbers[index-1]);
		}
	for (index = 1;index<=size;index++){
		currentSum = currentSum+numbers[index-1];
		if (currentSum>maxSum){
			maxSum = currentSum;
			}
		if (currentSum<0){
			currentSum = 0;
			}
		}
	printf("%d",maxSum);
	}
