#include<stdio.h>
int main() {
	char c;
	int l;
	int h;
	int d;
	scanf("%c",&c);
	l = (int)(c)>=(int)('A');
	h = (int)(c)<=(int)('Z');
	if (l && h){
		d = (int)(c)+32;
		}else{
		d = (int)(c)-32;
		}
	printf("%c",(char)(d));
	}
