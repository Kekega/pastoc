int main(){
int a[1005-1+1] ;
int n;
int i;
int max;
int x;
int br;
for (i = 1;i<=3;i++){
a[i-1] = 0;
}
scanf("%d",&n);
for (i = 1;i<=n;i++){
scanf("%d",&x);
a[x-1] = a[x-1]+1;
}
max = -1;
for (i = 1;i<=1005;i++){
if (max<a[i-1]){
max = a[i-1];
br = i;
}
}
printf("%d",br);
printf(" ");
printf("%d",max);
}
