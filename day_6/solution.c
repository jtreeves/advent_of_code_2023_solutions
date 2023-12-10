#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

int *extract_numbers(char *line)
{
    int *numbers = (int *)malloc(3 * sizeof(int));
    sscanf(strchr(line, ':') + 1, "%d %d %d", &numbers[0], &numbers[1], &numbers[2]);
    return numbers;
}

double *calculate_quadratic_formula(int quadratic_term, int constant_term)
{
    int signed_quadratic_term = -1 * quadratic_term;
    int discriminant = quadratic_term * quadratic_term - 4 * constant_term;
    double discriminant_root = sqrt(discriminant);
    double *result = (double *)malloc(2 * sizeof(double));
    result[0] = (signed_quadratic_term + discriminant_root) / 2;
    result[1] = (signed_quadratic_term - discriminant_root) / 2;
    return result;
}

void solution_6()
{
    char *data = extract_data_from_file(6, false);
    char **lines = get_list_of_lines(data);
    int *numbers = extract_numbers(lines[0]);
    int *times = extract_numbers(lines[0]);
    int *distances = extract_numbers(lines[1]);
    double *quadratic_results = calculate_quadratic_formula(-1 * times[0], distances[0]);
    printf("%s", data);
    printf("First line:");
    printf("%s", lines[0]);
    printf("Numbers: %d %d %d", numbers[0], numbers[1], numbers[2]);
    printf("RESULTS: %lf %lf", quadratic_results[0], quadratic_results[1]);
}
