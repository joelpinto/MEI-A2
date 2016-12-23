#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#define N 1000000
int matriz[N][3];

void insertionSort(int d, int n)
{
    int i;
    int j;
    int temp;
    int temp_aux;
    int temp_aux_aux;
    temp = matriz[i][0];
    j = i;
    if (d == 1) {
        for (i = 1;i < n;i++){
            temp = matriz[i][0];
            j = i - 1;
            while ((j >= 0) && (matriz[j][0] > temp)){
                matriz[j + 1][0] = matriz[j][0];
                j -= 1;
            }
            matriz[j + 1][0] = temp;
        }
    }else
        if (d == 2) {
            for (i = 1;i < n;i++){
                temp = matriz[i][0];
                temp_aux = matriz[i][1];
                j = i - 1;
                while ((j >= 0) && (temp < matriz[j][0] || (temp == matriz[j][0] && temp_aux < matriz[j][1]))){
                    matriz[j + 1][0] = matriz[j][0];
                    matriz[j + 1][1] = matriz[j][1];
                    j -= 1;
                }
                matriz[j + 1][0] = temp;
                matriz[j + 1][1] = temp_aux;
            }
        }else
            if (d == 3) {
                for (i = 1;i < n;i++){
                    temp = matriz[i][0];
                    temp_aux = matriz[i][1];
                    temp_aux_aux = matriz[i][2];
                    j = i - 1;
                    while ((j >= 0) && (temp < matriz[j][0] || (temp == matriz[j][0] && temp_aux < matriz[j][1]) || (temp == matriz[j][0] && temp_aux == matriz[j][1] && temp_aux_aux < matriz[j][2]))){
                        matriz[j + 1][0] = matriz[j][0];
                        matriz[j + 1][1] = matriz[j][1];
                        matriz[j + 1][2] = matriz[j][2];
                        j -= 1;
                    }
                    matriz[j + 1][0] = temp;
                    matriz[j + 1][1] = temp_aux;
                    matriz[j + 1][2] = temp_aux_aux;
                }
            }
}

int main()
{
    int n;
    int d;
    int i;
    int j;
    int aux;
    scanf("%d %d", &n, &d);
    if (n < 2 || n > 1000000) {
        return 0;
    }
    if (d < 1 || d > 3) {
        return 0;
    }
    for (i = 0;i < n;i++){
        for (j = 0;j < d;j++){
            scanf("%d", &aux);
            if (aux < (-999) || aux > 999) {
                return 0;
            }else
                matriz[i][j] = aux;
        }
    }
    clock_t start, end;
    start = clock();
    insertionSort(j, n);
    end = clock();
    printf("%f\n", (end - start) / (double)CLOCKS_PER_SEC * 1000.0f);
    return 0;
}
