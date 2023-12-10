#include <stdio.h>
#include <stdlib.h>
#include "utils/c/extract_data_from_file.c"
#include "utils/c/get_list_of_lines.c"
#include "day_1/solution.c"
// #include "day_2/solution.c"
#include "day_6/solution.c"

int main(int argc, char *argv[])
{
    // Check if at least one command-line argument is provided
    if (argc < 2)
    {
        fprintf(stderr, "Usage: %s requires an integer argument to determine which day's solution to execute\n", argv[0]);
        return 1;
    }

    // Convert the command-line argument to an integer
    int argument = atoi(argv[1]);

    // Use the argument to determine which function to run
    switch (argument)
    {
    case 1:
        printf("Running function 1\n");
        solution_1();
        // Call function 1 or perform relevant actions
        break;
    // case 2:
    //     printf("Running function 2\n");
    //     solution_2();
    //     // Call function 2 or perform relevant actions
    //     break;
    case 6:
        printf("Running function 6\n");
        solution_6();
        // Call function 2 or perform relevant actions
        break;
    default:
        fprintf(stderr, "Invalid argument: %d\n", argument);
        return 1;
    }

    return 0;
}
