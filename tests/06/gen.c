#include<stdio.h>
int main() {
	float a1;
	float b1;
	float a2;
	float b2;
	float p1;
	float p2;
	scanf("%f",&a1);
	scanf("%f",&b1);
	scanf("%f",&a2);
	scanf("%f",&b2);
	p1 = a1*b1/2;
	p2 = a2*b2/2;
	if (p1>p2){
		printf("1");
		}else{
		if (p1<p2){
			printf("2");
			}else{
			printf("0");
			}
		}
	}
