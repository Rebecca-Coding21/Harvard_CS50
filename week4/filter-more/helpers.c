#include "helpers.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int average;


    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float blue = image[i][j].rgbtBlue;
            float green = image[i][j].rgbtGreen;
            float red = image[i][j].rgbtRed;

            average = round((red + blue + green) / 3);
            //printf("Average: %i\n", average[i][j]);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    //printf("Average: %i\n", average[100][155]);

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE(*tmp_image)[width] = calloc(height, width * sizeof(RGBTRIPLE));

    for (int i = 0; i < height; i++)
    {
        //original images is saved in tmp_image
        for (int j = 0; j < width; j ++)
        {
            tmp_image[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j ++)
        {
            image[i][j] = tmp_image[i][width - (j + 1)];
        }
    }
    free(tmp_image);
    //free memory of tmp_image after usage
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE(*tmp_image)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    for (int i = 0; i < height; i++)
    {
        //original images is saved in tmp_image
        for (int j = 0; j < width; j ++)
        {
            tmp_image[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float counter = 0.0;
            int red = 0;
            int green = 0;
            int blue = 0;

            //loop over rows for each "pixel cube"
            for (int k = -1; k < 2; k++)
            {
                //loop over collums for each "pixel cube" (all surrounding pixels of current pixel)
                for (int l = -1; l < 2; l++)
                {
                    //check if surrounding pixel exists
                    if (i + k < height && j + l < width && i + k > -1 && j + l > -1)
                    {
                        red += tmp_image[i + k][j + l].rgbtRed;
                        blue += tmp_image[i + k][j + l].rgbtBlue;
                        green += tmp_image[i + k][j + l].rgbtGreen;
                        counter++;
                    }
                }

            }
            //change pixel in actual image to average
            image[i][j].rgbtRed = round(red / counter);
            image[i][j].rgbtBlue = round(blue / counter);
            image[i][j].rgbtGreen = round(green / counter);
        }
    }

    free(tmp_image);
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE(*tmp_image)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    for (int i = 0; i < height; i++)
    {
        //original image is saved in tmp_image
        for (int j = 0; j < width; j ++)
        {
            tmp_image[i][j] = image[i][j];
        }
    }
    //define Gx matrix
    int Gx [3][3] =
    {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };
    //define Gy matrix
    int Gy [3][3] =
    {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}
    };
    //loop through all pixels of the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //declare Gx and Gy for every colour channel
            int red_x = 0;
            int red_y = 0;
            int green_x = 0;
            int green_y  = 0;
            int blue_x = 0;
            int blue_y = 0;
            int counter = 0;

            for (int k = -1; k < 2; k++)
            {
                //loop over collums for each "pixel cube" (all surrounding pixels of current pixel)
                for (int l = -1; l < 2; l++)
                {
                    //check if surrounding pixel exists
                    if (i + k < height && j + l < width && i + k > -1 && j + l > -1)
                    {
                        // calculate Gx and Gy for every color chanel of every surrounding pixel (3x3)
                        red_x += (tmp_image[i + k][j + l].rgbtRed) * Gx[k + 1][l + 1];
                        blue_x += (tmp_image[i + k][j + l].rgbtBlue) * Gx[k + 1][l + 1];
                        green_x += (tmp_image[i + k][j + l].rgbtGreen) * Gx[k + 1][l + 1];
                        red_y += (tmp_image[i + k][j + l].rgbtRed) * Gy[k + 1][l + 1];
                        blue_y += (tmp_image[i + k][j + l].rgbtBlue) * Gy[k + 1][l + 1];
                        green_y += (tmp_image[i + k][j + l].rgbtGreen) * Gy[k + 1][l + 1];
                        counter++;
                    }
                }

            }
            //compute new chanel value
            int red_G = round(sqrt(pow(red_x, 2) + pow(red_y, 2)));
            int blue_G = round(sqrt(pow(blue_x, 2) + pow(blue_y, 2)));
            int green_G = round(sqrt(pow(green_x, 2) + pow(green_y, 2)));

            if (red_G > 255)
            {
                red_G = 255;
            }
            if (blue_G > 255)
            {
                blue_G = 255;
            }
            if (green_G > 255)
            {
                green_G = 255;
            }

            image[i][j].rgbtRed = red_G;
            image[i][j].rgbtGreen = green_G;
            image[i][j].rgbtBlue = blue_G;
        }
    }
    free(tmp_image);
    return;
}
