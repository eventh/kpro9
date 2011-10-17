#include struct_test
#define WORK_DAY 1
#define WEEKEND 2
#define HOLIDAY 3

enum gender{male,female = 0, alien, none};

struct its_just_a_model{

//enumtest
enum gender gend;
//arraytests
char chararr[2][2]
int intarr[2]
//bitstringtests
int flags;
short color;
//struct and struct within struct test
struct struct_test black_knight;
//enumerated named value test
int day;
}