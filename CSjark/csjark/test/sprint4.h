struct cpp_test {
#if defined(CONFIG_DEFINED) && defined(ARR)
    long double arr[ARR][CONFIG_DEFINED];
#endif
    float test;
#if defined(REMOVE)
    int failed;
#endif
};

struct placeholder_test {
    long *pointers[2];
};

enum months { JAN = 1, FEB, MAR, APR, NOV, DEC = 20 };

struct enum_arrays {
    enum months month_array[4];
};

