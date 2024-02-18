int main(){
int a[100-1+1] ;
int b[100-1+1] ;
int c[100-1+1] ;
int n;
int ai;
int bi;
int ci;
int i;
bi = 1;
ci = 1;
scanf("%d",&n);
for (ai = 1;ai<=n;ai++){
scanf("%d",&a[ai-1]);
}
for (ai = 1;ai<=n;ai++){
if (a[ai-1] % 2 == 0){
b[bi-1] = a[ai-1];
bi = bi+1;
}else{
c[ci-1] = a[ai-1];
ci = ci+1;
}
}
for (i = 1;i<=bi-1;i++){
printf("%d",b[i-1]);
printf(" ");
}
printf("\n");
for (i = 1;i<=ci-1;i++){
printf("%d",c[i-1]);
printf(" ");
}
}
