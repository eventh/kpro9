#define NUMFIVE 5
#define NUMTHREE 3

typedef struct twoints {
    int a;
    int b;
} twoints;

typedef enum media { FLOPPY = 1, CD = 3, DVD = 5 } media;

typedef union ageunion {
    int intage;
    char charage[3];
} ageunion;

typedef unsigned char BENQ;
typedef BENQ BENQTWO[2];
typedef BENQTWO BENQFOUR[2];
typedef twoints ARRAY[2];
typedef int INTPOINTER[3];
typedef media MEDIATWO[2];
typedef ageunion TWOAGEUNION[2];

struct typedef_test {
    int a;
    ARRAY b;
    long long int c;
    twoints d[NUMFIVE - NUMTHREE];
    short e;
    BENQFOUR f;
    signed int g;
    INTPOINTER h;
    unsigned int i;
    MEDIATWO j;
    float k;
    TWOAGEUNION l;
    double m;
};
