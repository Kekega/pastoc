#include<stdio.h>
int main() {
	int occurrences[1005-1+1] ;
	int size;
	int index;
	int maxOccurrence;
	int element;
	int resultElement;
	for (index = 1;index<=1005;index++){
		occurrences[index-1] = 0;
		}
	scanf("%d",&size);
	for (index = 1;index<=size;index++){
		scanf("%d",&element);
		occurrences[element-1] = occurrences[element-1]+1;
		}
	maxOccurrence = -1;
	for (index = 1;index<=1005;index++){
		if (maxOccurrence<occurrences[index-1]){
			maxOccurrence = occurrences[index-1];
			resultElement = index;
			}
		}
	printf("%d",resultElement);
	printf(" ");
	printf("%d",maxOccurrence);
	}
