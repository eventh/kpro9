#define NAME_LENGTH 10

struct postcode {
    int code;
    char place[NAME_LENGTH];
};

struct user {
    char username[NAME_LENGTH];
    char password[NAME_LENGTH];
};

struct name {
    char first_name[NAME_LENGTH];
    char last_name[NAME_LENGTH];
};

struct user_and_name{
    struct user u1;
    struct name n1;
};

struct struct_test {
    int id;
    struct user_and_name username;
    char adress[NAME_LENGTH];
    int number;
    struct postcode pcode;
};
