#include "time.h"

#define ARRAY_SIZE 2

typedef signed int BOOL;
typedef enum {TRUE, FALSE} bool_t;
typedef int array[5];

enum repeat{and=1, elseif, in=412};

struct local {
    int end;
};

struct keyword_test {
    int in;
    int until[ARRAY_SIZE][ARRAY_SIZE];
    int _VERSION;
    enum repeat function;
    struct local or;
    int and;
    int _and;
    int not;
};

struct abcde {
	int a;
	int b;
	long c;
	short d;
	char e;
};

struct alignment_test {
	int a;
	short b;
	char c;
	char d;
	char e;
	struct abcde f;
};


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

struct platform_test {
    // Tests wildcard support for unknown types (known sizes)
    long double bytes;

    // Test windows platform
    signed a;
#if _WIN32
    float win_float;
#else
    _Bool plat;
#endif
    char b;
#if _M_X64
    unsigned int intel64;
#endif

    // Test union
    union {
        int a;
#if __sun
        float something;
#endif
        char arr[4];
#if __APPLE__
        int apple;
#endif
    } anom;

    // Test that correct sizes are used
    long int deff;
#if _M_IX86
    long int intel;
#endif
#if __sparc
    unsigned long int sparc;
#endif
#if _WIN64
    signed long int win64;
#endif
};

union union_test {
    int int_member;
    float float_member;
    unsigned long long long_long_member;
};

struct union_within_struct {
    int a;
    union union_test union_member;
    float b;
};

