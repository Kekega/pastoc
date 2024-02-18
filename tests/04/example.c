void check_arm(int x, int cj, int cd, int cs) {
	if(x < 0) {
		return;
	}
	int arm = x == cj * cj * cj + cd * cd * cd + cs * cs * cs;
	if(arm) {
		printf("YES");
	} else {
		printf("NO");
	}
}
int main() {
	int j, cj, cd, cs;
	scanf("%d", &j);
	cj = j % 10;
	cd = (j / 10) % 10;
	cs = (j / 100) % 10;
	check_arm(j, cj, cd, cs);
	return 0;
}
