#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{

    string text = get_string("Text: ");
    int letters = 0;
    int words = 1;
    int sentences = 0;
    int n = strlen(text);

    for (int i = 0; i < n ; i++)
    {
        //Capital letters become small letters
        if (isupper(text[i]))
        {
            text[i] = tolower(text[i]);
        }
        //count letters
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            letters = letters + 1;
        }
        //count words
        else if (text[i] == ' ')
        {
            words = words + 1;
        }
        //count sentences
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences = sentences + 1;
        }
    }
    //calculate index
    float L = ((float) letters / (float) words) * 100;
    float S = ((float) sentences / (float) words) * 100;
    float index = 0.0588 *  L -  0.296 *  S - 15.8;
    //round the index
    int grade = round(index);

    printf("L: %f\n", L);
    printf("S: %f\n", S);

    //print grade
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }

}