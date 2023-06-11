// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    //Variable of datatype file named input, * = arrow to location where value of variable can be find
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    //Variable of datatype file named output, * = arrow to location where value of variable can be find
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file

    uint8_t header [HEADER_SIZE];

    fread(header, HEADER_SIZE, 1, input);
    //data with size of header_size(=44 Bytes), 1 datatype( int) from input, which is file input.wav is stored in array header
    fwrite(header, HEADER_SIZE, 1, output);
    //data with size 44 Bytes is written from array header to output file (1 datatype)

    // TODO: Read samples from input file and write updated data to output file

    int16_t buffer;                         //woher weiß Programm wann Header vorbei ist und buffer anfängt?
    while (fread(&buffer, 2, 1, input))
    {
        buffer *= factor;
        fwrite(&buffer, 2, 1, output);
    }




    // Close files
    fclose(input);
    fclose(output);
}
