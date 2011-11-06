struct cpp_test {
#if defined(CONFIG_DEFINED) && defined(ARR)
    long double arr[ARR][CONFIG_DEFINED];
#endif

#if defined(REMOVE)
    int failed;
#endif
};

