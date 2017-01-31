#include <stdio.h>
#include <stdlib.h>
void printArray(int* array, int size)
{
    int i;
    printf("[ ");
    for (i = 0;i < size;i++)
        printf("%d ", array[i]);
    printf("]\n");
}

int findLargestNum(int* array, int size)
{
    int i;
    int largestNum = array[0];
    for (i = 0;i < size;i++){
        if (array[i] > largestNum) 
            largestNum = array[i];
    }
    return largestNum;
}
void radixsorte(int* array, int size)
{
    printf("\n\nRunning Radix Sort on Unsorted List!\n\n");
    int i;
    int semiSorted[size];
    int significantDigit = 1;
    int largestNum = findLargestNum(array, size);
    while (largestNum / significantDigit > 0){
        printf("\tSorting: %d's place ", significantDigit);
        printArray(array, size);
        int bucket[10] = {0};
        for (i = 0;i < size;i++)
            bucket[(array[i] / significantDigit) % 10]++;
        for (i = 1;i < 10;i++)
            bucket[i] += bucket[i - 1];
        for (i = size - 1;i >= 0;i--)
            semiSorted[--bucket[(array[i] / significantDigit) % 10]] = array[i];
        for (i = 0;i < size;i++)
            array[i] = semiSorted[i];
        significantDigit *= 10;
    }
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
    radixsorte(*matriz, n);
    printArray(*matriz, n);
    for (i = 0;i < n;i++){
        for (j = 0;j < d;j++){
            printf("%d", matriz[i][j]);
            if (j < d - 1) 
                printf(" ");
        }
        printf("\n");
    }
    return 0;
}
