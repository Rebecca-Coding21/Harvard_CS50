#include <stdio.h>
#include <cs50.h>

int main (void)
{
    string answer = get_string("Wie heißt du?\n");
    printf("hello,%s\n",answer);
}