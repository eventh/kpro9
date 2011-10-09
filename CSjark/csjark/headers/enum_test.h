#define STRING_LEN 10

#define MONDAY 1
#define TUESDAY 2
#define WEDNESDAY 3
#define THURSDAY 4
#define FRIDAY 5
#define SATURDAY 6
#define SUNDAY 7

struct enum_test {
	int id;
	char name[STRING_LEN];
	int weekday;
};
