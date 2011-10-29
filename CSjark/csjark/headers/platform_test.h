
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
#if __ia64
    unsigned intel64;
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
