#include <stdio.h>
#include <stdlib.h>

int getMax(int** arr, int n){
    int mx = *arr[0];
    for (int i = 1; i < n; i++){
        if (*arr[i] > mx){
            mx = *arr[i];
        }
    }
    printf("mx:%d\n",mx);    
    return mx;
}

void countSort(int** arr, int n, int exp){
    int output[n];
    int i, count[10] = {0};
 
    for (i = 0; i < n; i++)
        count[ (*arr[i]/exp)%10 ]++;
 
    for (i = 1; i < 10; i++)
        count[i] += count[i - 1];
 
    for (i = n - 1; i >= 0; i--){
        output[count[ (*arr[i]/exp)%10 ] - 1] = *arr[i];
        count[ (*arr[i]/exp)%10 ]--;
    }

    for (i = 0; i < n; i++)
        *arr[i] = output[i];
}
 
void radixsorte(int** arr, int primeiro, int ultimo, int n){
    int m = getMax(arr, n);



    for (int exp = 1; m/exp > 0; exp *= 10)
        countSort(arr, n, exp);
}

void print(int** arr, int n){
	int i;
	printf("[ ");
	for (i = 0; i < n; i++)
		printf("%d ", *arr[i]);
	printf("]\n");
}
 

int main(){
	int i, j,num,n,d;
	int **matriz;

	scanf("%d %d",&n,&d);

	if(n<2 || n>1000000)
		return 0;

	matriz = (int **)malloc(n*sizeof(int*));

	if(d<1 || d>3)
		return 0;

	for(i=0;i<n;i++){
		matriz[i] = (int *)malloc(d*sizeof(int));
		for(j=0;j<d;j++){
			scanf("%d",&num);
			if(num<(-999) || num>999)
				return 0;
			else
				matriz[i][j]=num;
		}
	}

	radixsorte(matriz, 0, n-1, n);
	print(matriz,n);
	
	for(i=0;i<n;i++){
		for(j=0;j<d;j++){
			printf("%d",matriz[i][j]);
			if(j<d-1)
                printf(" ");
		}
		printf("\n");
	}
	return 0;
}