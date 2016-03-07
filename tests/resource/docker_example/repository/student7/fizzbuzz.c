#include <stdio.h>
#include <limits.h>
int main(int argc, char *argv[])
{
	for (unsigned int i = 0; i< UINT_MAX; i++)
		for (unsigned int j = 0; j< UINT_MAX; j++)
			for (unsigned int k = 0; k< UINT_MAX; k++)
				printf("testing\n");
	return 0;
}
