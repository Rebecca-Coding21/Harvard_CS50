#include <cs50.h>
#include <stdio.h>

int main (void)
{
    int startPop;
    int i;
    int endPop;
    // TODO: Prompt for start size
    do
    {
          startPop = get_int("Start size: ");
    }
    while(startPop<9);
// TODO: Prompt for end size
    do
    {
        endPop = get_int("End size: ");
    }
    while(endPop<startPop);


    // TODO: Calculate number of years until we reach threshold
    int curPop = startPop;
    int maxJahre = 0;


    while(curPop<endPop)
    {
        curPop = curPop + (curPop/3) - (curPop/4);
        maxJahre = maxJahre + 1;
    }

    printf("Years: %i\n", maxJahre);

}