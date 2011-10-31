#include "cenum_test.h"

union testUnion{
    int int_member;
    struct cenum_test cenum_test_member;
    long long long_long_member;
    short short_member;
};

typedef union testUnion typedef_union;

typedef struct {
    int a;
    int b;
} typedef_struct;

typedef int int_array[4];

struct complex_array_test {
    char chararr1[16];
    union testUnion test_union_array[4];
    typedef_union typedef_union_array[6];
    int intarr2[2][2][2][2];
    struct cenum_test struct_array[4];
    typedef_struct typedef_struct_array[4];
    int_array int_array_array[4];
};
