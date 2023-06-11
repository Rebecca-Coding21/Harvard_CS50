// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 500; //number of lines in the hash table (26 letters)

// Hash table
node *table[N];
int word_number = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // hash word to get it's hash value
    int hash_value = hash(word);

    //access linked list at index in hash table
    node *n = table[hash_value];

    while (n != NULL)
    {

        if (strcasecmp(n->word, word) == 0)
        {
            return true;
        }

        n = n->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    long sum = 0;

    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }
    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *input_dict = fopen(dictionary, "r");

    if (input_dict == NULL)
    {
        return false; //false if file is empty
    }

    char tmp_word[LENGTH + 1];

    while (fscanf(input_dict, "%s", tmp_word) != EOF)
    {
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        strcpy(n->word, tmp_word);

        int hash_value = hash(tmp_word);
        n->next = table[hash_value];        //new node points to hash-table line (from hash_value)
        table[hash_value] = n;
        word_number++;

    }
    fclose(input_dict);

    return true;

}


// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{

    return word_number;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];

        while (n != NULL)
        {
            node *tmp = n;
            n = n->next;
            free(tmp);
        }

        if (n == NULL && i == N - 1)
        {
            return true;
        }
    }
    return false;
}
