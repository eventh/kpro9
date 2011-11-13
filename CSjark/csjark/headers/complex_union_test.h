#include "union_test.h"
#include "cenum_test.h"

typedef signed int BOOL;
typedef enum {TRUE, FALSE} bool_t;

typedef union {
    int int_member;
    struct cenum_test cenum_test_member;
    long long long_long_member;
    BOOL bool_member;
    bool_t bool_t_member;
    short short_member;
} complex_union;

struct struct_with_complex_union {
    complex_union complex_union_member;
    bool_t bool_t_member;
    union union_test union_test_member;
};

