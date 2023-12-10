#include <stdlib.h>
#include <string.h>

char **get_list_of_lines(char *block)
{
    int line_count = 1;
    for (char *c = block; *c != '\0'; ++c)
    {
        if (*c == '\n')
        {
            line_count++;
        }
    }
    char **lines = (char **)malloc(line_count * sizeof(char *));
    int line_index = 0;
    char *start = block;
    for (char *c = block; *c != '\0'; ++c)
    {
        if (*c == '\n' || *(c + 1) == '\0')
        {
            lines[line_index] = (char *)malloc((c - start + 2) * sizeof(char));
            strncpy(lines[line_index], start, c - start + 1);
            lines[line_index][c - start + 1] = '\0';
            start = c + 1;
            line_index++;
        }
    }
    return lines;
}
