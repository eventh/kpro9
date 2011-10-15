#define STRING_LENGTH 10
#define ADEFINE 5

#define BLACK 1
#define RED 2
#define BLUE 3
#define YELLOW 4
#define WHITE 5
#define GREEN 6
#define ORANGE 7

enum color { black=16, white=32, gray=48, green=64, yellow=80, blue=96, cyan=112, punk=128, red=144 };
enum weekday { monday = 1, tuesday, wedenesday, thursday, friday, saturday, friday };

/* Struct to test different configs in sprint II */
struct config_test {
    /* Some members */
    int id;
    char name[STRING_LENGTH];
    /*enum config test */
    short int shortint1;
    int enumcolor;
    short int shortin2;
    /* enum datatype test */
    enum color colors;
    enum weekday day;
    /* bit string test */
    short shortbitstring;
    int intbitstring;
    unsigned int uintbitstring;
    unsigned long longbitstring;
    unsigned long int typebitstring;
    /* array test */
    int array_1d[2];
    long array_2d[2][2];
    short array_3d[2][2][2];
    char array_4d[2][2][2][2];
    /* range test */
    short age;
    short percent;
	/* more test */
};
