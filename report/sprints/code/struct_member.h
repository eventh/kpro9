#define NAME_LENGTH 10

struct postcode {
    int code;
    char town[NAME_LENGTH];
};

struct struct_member {
    int uid;
    struct postcode pcode;
};