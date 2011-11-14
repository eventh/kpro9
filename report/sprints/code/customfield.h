#include "time.h"

typedef signed int BOOL;

struct custom_lua {
    time_t abs;
    time_t rel;
    BOOL bol;
    int all;
};
