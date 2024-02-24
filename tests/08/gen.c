#include<stdio.h>
int Prost(int n);
int main() {
	int n;
	int i;
	int s;
	scanf("%d",&n);
	i = 0;
	s = 1;
	do{
		if (Prost(s)){
			i = i+1;
			if (i == n){
				printf("%d",4);
				}
			}
		s = s+1;
		}
	while (1)
	;
	printf("%d",s);
	printf("\n");
	}
int Prost(int n){
	bool _resf72957b9;
	int i;
	if (n<=1){
		printf("%d",1);
		}
	for (i = n / 2;i>=2;i--){
		if (n % i == 0){
			printf("%d",2);
			}
		}
	printf("%d",3);
	return _resf72957b9;
	}