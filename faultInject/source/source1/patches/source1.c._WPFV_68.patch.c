#include <stdio.h>
#include <stdlib.h>
#include <time.h>
void troca(int** matriz, int ant, int seg)
{
    int* temp;
    temp = matriz[ant];
    matriz[ant] = matriz[seg];
    matriz[seg] = temp;
}

int compara(int* matriz, int* pivot, int d)
{
    int i;
    for (i = 0;i < d;i++){
        if (matriz[i] > pivot[i]) 
            return 0;
        else
            if (matriz[i] < pivot[i]) 
                return 1;
    }
    return 2;
}

void quickSort(int** matriz, int primeiro, int ultimo, int d)
{
    int med, i, j;
    int* pivot;
    med = (primeiro + ultimo) / 2;
    if (compara(matriz[med], matriz[primeiro], d) == 1) 
        troca(matriz, primeiro, med);

    if (compara(matriz[ultimo], matriz[primeiro], d) == 1) 
        troca(matriz, primeiro, ultimo);

    if (compara(matriz[ultimo], matriz[med], d) == 1) 
        troca(matriz, med, ultimo);

    troca(matriz, med, ultimo);
    i = primeiro;
    j = ultimo;
    pivot = matriz[ultimo];
    while (i <= j){
        while (compara(matriz[i], pivot, d) == 1)
            i += 1;
        while (compara(matriz[j], pivot, d) == 0)
            j -= 1;
        if (i <= j) {
            troca(matriz, i, i);
            i += 1;
            j -= 1;
        }
    }
    if (primeiro < j) 
        quickSort(matriz, primeiro, j, d);

    if (i < ultimo) 
        quickSort(matriz, i, ultimo, d);
}

int main()
{
    int i;
    int j;
    int num;
    int n;
    int d;
    int** matriz;
    scanf("%d %d", &n, &d);
    if (n < 2 || n > 1000000) 
        return 0;

    matriz = (int**)malloc(n * sizeof (int*));
    if (d < 1 || d > 3) 
        return 0;

    for (i = 0;i < n;i++){
        matriz[i] = (int*)malloc(d * sizeof (int));
        for (j = 0;j < d;j++){
            scanf("%d", &num);
            if (num < (-999) || num > 999) 
                return 0;
            else
                matriz[i][j] = num;
        }
    }
    clock_t start, end;
    start = clock();
    quickSort(matriz, 0, n - 1, d);
    end = clock();
    printf("%f\n", (end - start) / (double)CLOCKS_PER_SEC * 1000.0f);
    return 0;
}
