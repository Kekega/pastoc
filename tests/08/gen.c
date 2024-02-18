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
				break;
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
	bool _resdcb2a15f;
	int i;
	if (n<=1){
		exit(0);
		}
	for (i = n / 2;i>=2;i--){
		if (n % i == 0){
			exit(0);
			}
		}
	exit(1);
	return _resdcb2a15f;
	}