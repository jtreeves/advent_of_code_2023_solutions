#include <stdio.h>
#include <stdbool.h>

char *extract_data_from_file(int day_number, bool is_official)
{
    char *name = (is_official) ? "data" : "practice";
    char file_path[20];
    snprintf(file_path, sizeof(file_path), "day_%d/%s.txt", day_number, name);
    FILE *file = fopen(file_path, "r");
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    rewind(file);
    char *data = (char *)malloc(file_size + 1);
    fread(data, 1, file_size, file);
    data[file_size] = '\0';
    fclose(file);
    return data;
}
