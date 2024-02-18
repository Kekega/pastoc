#include<stdio.h>
void check_arm(int x, int cj, int cd, int cs);
int main() {
	int j;
	int cj;
	int cd;
	int cs;
	scanf("%d",&j);
	cj = j % 10;
	cd = j / 10 % 10;
	cs = j / 100 % 10;
	check_arm(j, cj, cd, cs);
	}
void check_arm(int x, int cj, int cd, int cs){
	int arm;
	if (x<0){
		exit;
		}
	arm = x == cj*cj*cj+cd*cd*cd+cs*cs*cs;
	if (arm){
		printf("YES");
		}else{
		printf("NO");
		}
	}