#include <stdio.h>
#include <stdlib.h>
#define num_rows 3
#define num_cols 3

int main(int argc, char* argv[]){
	int a[num_rows][num_cols] = {
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9}
	};

	int b[num_rows][num_cols] = {
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9}
	};

	int c[num_rows][num_cols];

	int i = 0;
	int j = 0;
	int k = 0;
	int sum = 0;

	#pragma omp parallel num_threads(4)
	{
		#pragma omp for
		for(i = 0; i < num_rows; i++){
			for(j = 0; j < num_cols; j++){
				sum = 0;
				for(k = 0; k < num_cols; k++){
					sum += a[i][k] * b [k][j];
				}
				c[i][j] = sum;
			}
		}	
	}
	
	for(i = 0; i < num_rows; i++){
		for(j = 0; j < num_cols; j++){
			printf("%d\t", c[i][j]);
		}
		printf("\n");
	}

	return 0;
}