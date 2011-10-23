#include "time.h"

typedef signed int BOOL;

struct custom_lua {
    /* Fields tests */
    time_t abs;
    time_t rel;
    BOOL bol;
    int all;
};
