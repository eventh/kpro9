struct platform_test {
    signed a;
#if _WIN32
    float plat;
#else
    _Bool plat;
#endif
    char b;
};
