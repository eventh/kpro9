union cunion_test {
    int int_member;
    float float_member;
    unsigned long long long_long_member;
};

struct union_within_struct {
    int a;
    union cunion_test union_member;
    float b;
};

    
    