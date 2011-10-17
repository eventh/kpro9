#define STRING_LEN 10

struct array_test {
    char chararr1[16];
    int intarr2[4][4];
    char chararr3[2][3];
    float floatarr4[1][2][3];
};

struct bitstring_test {
    int id;
    int flags;
    short color1;
    short color2;
};

enum Months {
    JAN = 1, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC = 20
};

struct cenum_test {
    int id;
    enum Months mnd;
};

struct enum_test {
    int id;
    char name[STRING_LEN];
    int weekday;
    int number;
};

struct range_test {
    char name[STRING_LEN];
    int age;
};

