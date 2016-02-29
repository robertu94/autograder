#include <stdio.h>

int main(int argc, char *argv[])
{
	int i;
	
	if (argc != 2) return 1;
	if (sscanf(argv[1], "%d", &i) != 1) return 1;

	if (i % 3 == 0){
		printf("fizz");
	}
	if (i % 2 == 0){
		printf("buzz");
	}
	printf("\n");
	return 0;
}
