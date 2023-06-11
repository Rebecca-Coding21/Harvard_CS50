#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>


char alphabet[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};



int main(int argc, string argv[])
{

    if (argc == 1)     //Error Message if no key
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }


    string key  = argv[1];
    int length = strlen(key);
    //string ciphertext;


    //check if length = 26 characters
    if (length < 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }


    for (int i = 0; i < length; i++)
    {

        for (int j = 0; j < length; j++)
        {
            if (i == j)
            {
                continue;
            }

            if (key[i] == key[j])
            {
                printf("Every letter must exist only once!\n");
                return 1;

            }

        }
    }

    for (int i = 0; i < length; i++)
    {

        int ascci = (int) key[i];

        if (ascci < 65 || (ascci > 90 && ascci < 97) || ascci > 122)
        {
            printf("key must only contain letters!\n");
            return 1;
        }
    }


    //Convert plaintext to ciphertext

    string plaintext = get_string("Plaintext:");
    string ciphertext = plaintext;
    int n = strlen(plaintext);
    int j;

    for (int i = 0; i < n; i++)   //Plaintext
    {

        for (j = 0; j < 26; j++)            //Adresses every letter of Plaintext to the number in the alphabet
        {

            if (islower(plaintext[i]))
            {
                //PLAINTEXT BECOMES CAPITAL LETTER
                if (plaintext[i] == tolower(alphabet[j]))
                {

                    ciphertext[i] = tolower(key[j]);

                    break;
                }
            }
            else if (isupper(plaintext[i]))
            {
                if (plaintext[i] == (alphabet[j]))
                {

                    ciphertext[i] = toupper(key[j]);
                    break;
                }
            }

        }

    }


    printf("ciphertext: %s\n", ciphertext);


}

