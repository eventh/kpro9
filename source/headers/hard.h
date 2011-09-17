#include "headers\stdbool.h"

#define ITEMS 10
#define STRING_LEN 30

// Shorthand structure with typedef keyword
typedef struct {
    int a;
    float b;
} simple;

enum cardsuit {
   CLUBS,
   DIAMONDS,
   HEARTS,
   SPADES
};

struct basic {
    // Boolean
    bool test;

    // Array
    char name[STRING_LEN];
    int values[ITEMS];

    // Enum
    enum cardsuit suit;

    // Union
    union {
        int a;
        float b;
    } car;

    // Struct
    simple a_struct;

    // Pointers (not a requirement)
    int *pointer;
    struct basic *self;
};
