#include<stdio.h>
int main() {
	char c;
	int lo;
	int hi;
	int d;
	scanf("%c",&c);
	lo = c>='A';
	hi = c<='Z';
	if (lo && hi){
		d = c+32;
		}else{
		d = c-32;
		}
	printf("%c",d);
	}
