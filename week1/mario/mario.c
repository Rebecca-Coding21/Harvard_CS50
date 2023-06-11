#include <cs50.h>
#include <stdio.h>

int main (void)
{
    int height;
    do
    {
        height = get_int("Height:\n");
    }
    while(height>8 || height < 1);

    int width = height * 2 + 2;
    int h;
    int w;

    //outer loop
    for(h = 0; h<height; h++)
    {

        // inner loop
        for(w = 0; w<width; w++)
        {


            if(w < height -h - 1 || (height - 1  < w && w < height + 2))
            {
                printf(" ");
            }
           else if(w> width - height + h)
            {
                break;
            }
           else
           {
               printf("#");
           }


        }
        printf("\n");
    }

}