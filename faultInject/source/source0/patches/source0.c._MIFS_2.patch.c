# include<stdio.h>
# include<stdlib.h>
#define TAM 1000
void quick(int vet[], int esq, int dir)
{
    int pivo = esq, i, ch, j;
    for (i = esq + 1;i <= dir;i++){
        j = i;
        if (vet[j] < vet[pivo]) {
            ch = vet[j];
            while (j > pivo){
                vet[j] = vet[j - 1];
                j--;
            }
            vet[j] = ch;
            pivo++;
        }
    }
    if (pivo - 1 >= esq) {
        quick(vet, esq, pivo - 1);
    }
}

int main()
{
    int vet[TAM], i, j;
    i = 0;
    while (scanf("%d", &vet[i]) == 1)
        i++;
    quick(vet, 0, i - 1);
    for (j = 0;j < i;j++)
        printf("%d\n", vet[j]);
    return 0;
}
