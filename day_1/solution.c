#include <stdio.h>
#include <stdlib.h>
#include "../utils/c/add_two_numbers.c"

int solution_1()
{
    printf("Hello, World!\n");
    int result = add_two_numbers(5, 6);
    printf("The sum is %d\n", result);

    FILE *file = fopen("day_1/practice_1.txt", "r");

    // Find the size of the file
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    rewind(file);

    // Allocate memory for the string
    char *content = (char *)malloc(file_size + 1);

    fread(content, 1, file_size, file);
    // Read the contents of the file into the string
    // if (fread(content, 1, file_size, file) != file_size)
    // {
    //     perror("Error reading the file");
    //     fclose(file);
    //     free(content);
    //     return 1;
    // }

    // Null-terminate the string
    content[file_size] = '\0';

    // Print or process the content as needed
    printf("File content:\n%s\n", content);

    // Close the file and free the allocated memory
    fclose(file);
    free(content);

    return 0;
}
