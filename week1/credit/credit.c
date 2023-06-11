#include <stdio.h>
#include <cs50.h>
#include <math.h>



int main (void)
{
    //prompt user for creditcard number
   long cardnumber = get_long("Number: ");

    //svariable declaration
    int sum2 = 0;
    int sum1 = 0;
    int digitI;
    int digitIndex2 = 0;
    int digitIndex1= 1;
    int m = 1;
    int endSum;
    int product;

    int digitNum = 1;

    long cardnumberNeu = cardnumber;

    //get number of digits
    while (cardnumberNeu>=10)
    {
        cardnumberNeu = (long)(cardnumberNeu / 10);
        digitNum++;

    }



    int length = digitNum;

    //get every second digits and calculate sum

    for(m = 1; m < length; m += 2)
    {
        long exponent = pow(10, m);
        digitIndex2 = digitIndex2 + 2;
        digitI = (cardnumber / exponent) % 10;

        product = digitI * 2;

        if (product > 9)
        {
            sum2 = sum2 + (product % 10) + ((product / 10) %10);

        }
        else
        {
           sum2 = sum2 + product;
        }

    }
    //get every first digit and calculate sum
    for(m = 0; m < length; m += 2)
    {
        long exponent = pow(10, m);
        digitI = (cardnumber / exponent) % 10;
        //printf("Digit-Nr. %i:%i\n", digitIndex1, digitI);
        digitIndex1 = digitIndex1 + 2;
        sum1 = sum1 + digitI;
    }

    digitIndex1 = digitIndex1 - 2;

    //calculate end sum
    endSum = sum1 + sum2;

    //get number number of first and second digit
    long exponent1 = pow(10, (length-1));
    int digit1 = (cardnumber / exponent1) %10;

    long exponent2 = pow(10, (length - 2));
    int digit2 = (cardnumber / exponent2) %10;

    int endsumEnd = endSum % 10;

    //get cardtype

    if(endSum % 10 == 0 && digit1 == 3 && (digit2 == 4 || digit2 == 7)&& length == 15)
    {
       printf("AMEX\n");
    }
    else if(endSum %10 == 0 && digit1 == 4 &&  (length == 16 || length == 13))
    {
        printf("VISA\n");
    }
    else if(endSum % 10 == 0 && digit1 == 5 && (digit2 > 0 && digit2 < 6) && length == 16 )
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }
}