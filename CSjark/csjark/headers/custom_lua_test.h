#include <time.h>

typedef signed int BOOL;
typedef enum {TRUE, FALSE} bool_t;
typedef int array[5];

struct custom_lua {
    short normal;
    long long special;

    /* Custom Fields tests */
    time_t abs;
    time_t rel;
    BOOL bol;
    int all;

    /* Custom Lua files tests */
    bool_t truth;
    array five;
    int *pointer;
    char str[4][3][2];
};
