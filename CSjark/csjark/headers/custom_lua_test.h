#include "time.h"

typedef signed int BOOL;

struct custom_lua {
    short normal;
    long long special;
};

struct field_test {
    time_t abs;
    time_t rel;
    BOOL bol;
    int all;
};
