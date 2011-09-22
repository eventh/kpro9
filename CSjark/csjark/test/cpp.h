/*
   A header file for testing the C preprocessor
   Used in parser.py
*/

#define TEST 10

// Test #include
#define PLEASE_INCLUDE
#ifdef PLEASE_INCLUDE
#include "include.h"
#endif

struct simple {
    int arr[TEST];
};

struct hard {
    bool boolean[HARD];
};
